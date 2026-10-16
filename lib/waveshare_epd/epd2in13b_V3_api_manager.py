"""WaveShare e-Ink 2in13b_V3 Display API Manager"""
import os
import logging
import time
import threading
from enum import Enum
from PIL import Image, ImageDraw, ImageFont
from .epd2in13b_V3 import EPD
from lib.common.IotError import EinkDisplayManagerError

logger = logging.getLogger(__name__)


class Zone(Enum):
    TOP_LEFT      = "top_left"
    TOP_RIGHT     = "top_right"
    MIDDLE_CENTER = "middle_center"
    BOTTOM_LEFT   = "bottom_left"
    BOTTOM_RIGHT  = "bottom_right"


_ZONE_CONFIG = {
    Zone.TOP_LEFT:      {"x": 4,   "y": 4,  "font_size": 18, "layer": "black", "anchor": "lt"},
    Zone.TOP_RIGHT:     {"x": 208, "y": 4,  "font_size": 18, "layer": "black", "anchor": "rt"},
    Zone.MIDDLE_CENTER: {"x": 106, "y": 52, "font_size": 28, "layer": "red",   "anchor": "mm"},
    Zone.BOTTOM_LEFT:   {"x": 4,   "y": 99, "font_size": 18, "layer": "black", "anchor": "lb"},
    Zone.BOTTOM_RIGHT:  {"x": 208, "y": 99, "font_size": 18, "layer": "black", "anchor": "rb"},
}


class EinkDisplayManager:

    def __init__(self):
        self._epd = EPD()
        self._state = {zone: "" for zone in Zone}
        self._is_initialized = False
        self._last_refresh_time = 0.0
        self._stale_timer = None

        font_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),
            "pic", "Font.ttc"
        )
        self._fonts = {
            18: ImageFont.truetype(font_path, 18),
            28: ImageFont.truetype(font_path, 28),
        }

    def init(self):
        result = self._epd.init()
        if result != 0:
            raise EinkDisplayManagerError(f"EPD init failed with code {result}")
        self._is_initialized = True

    def clear(self):
        self._epd.Clear()
        self._state = {zone: "" for zone in Zone}

    def sleep(self):
        self._cancel_stale_timer()
        self._epd.sleep()
        self._is_initialized = False

    def _cancel_stale_timer(self):
        if self._stale_timer is not None:
            self._stale_timer.cancel()
            self._stale_timer = None

    def set_zone(self, zone: Zone, text: str):
        if not isinstance(zone, Zone):
            raise EinkDisplayManagerError(f"Invalid zone: {zone!r}")
        self._state[zone] = text

    def refresh(self):
        """Render current zone state to the display.

        WARNING: After calling refresh(), always call sleep() (or use the context
        manager) once your update session is complete. Leaving the display powered
        indefinitely after a refresh keeps it in a high-voltage state and will cause
        irreversible hardware damage (Waveshare hardware precaution).
        """
        if not self._is_initialized:
            raise EinkDisplayManagerError("Display is not initialized; call init() first")
        if self._last_refresh_time != 0.0 and time.time() - self._last_refresh_time < 180:
            logger.warning("refresh() called within 180 s of the previous refresh")

        black_img = Image.new('1', (212, 104), 255)
        red_img   = Image.new('1', (212, 104), 255)
        draw = {"black": ImageDraw.Draw(black_img), "red": ImageDraw.Draw(red_img)}

        for zone, text in self._state.items():
            if not text:
                continue
            cfg = _ZONE_CONFIG[zone]
            draw[cfg["layer"]].text(
                (cfg["x"], cfg["y"]),
                text,
                font=self._fonts[cfg["font_size"]],
                fill=0,
                anchor=cfg["anchor"],
            )

        self._epd.display(self._epd.getbuffer(black_img), self._epd.getbuffer(red_img))
        self._last_refresh_time = time.time()

        self._cancel_stale_timer()
        self._stale_timer = threading.Timer(86400, self._force_refresh)
        self._stale_timer.daemon = True
        self._stale_timer.start()

    def update_zone(self, zone: Zone, text: str):
        self.set_zone(zone, text)
        self.refresh()
