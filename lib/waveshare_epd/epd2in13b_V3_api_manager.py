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
