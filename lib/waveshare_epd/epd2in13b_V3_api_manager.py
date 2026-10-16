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
