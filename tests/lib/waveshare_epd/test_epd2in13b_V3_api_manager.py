import sys
from unittest.mock import MagicMock, patch

from lib.common.IotError import EinkDisplayManagerError

mock_epdconfig = MagicMock()
mock_epdconfig.RST_PIN = 11
mock_epdconfig.DC_PIN = 25
mock_epdconfig.BUSY_PIN = 24
mock_epdconfig.CS_PIN = 8

sys.modules['lib.waveshare_epd.epdconfig'] = mock_epdconfig

from lib.waveshare_epd import epd2in13b_V3_api_manager
from lib.waveshare_epd.epd2in13b_V3_api_manager import EinkDisplayManager, Zone


class TestEinkDisplayManager:

    def setup_method(self):
        mock_epdconfig.reset_mock(side_effect=True)
        mock_epdconfig.RST_PIN = 11
        mock_epdconfig.DC_PIN = 25
        mock_epdconfig.BUSY_PIN = 24
        mock_epdconfig.CS_PIN = 8

        with patch.object(epd2in13b_V3_api_manager, 'EPD') as mock_epd_class, \
             patch.object(epd2in13b_V3_api_manager, 'ImageFont') as mock_font:
            self.mock_epd = mock_epd_class.return_value
            self.mock_font = mock_font
            self.mgr = EinkDisplayManager()

    # ------------------------------------------------------------------
    # __init__
    # ------------------------------------------------------------------

    def test_constructor_initializes_state(self):
        # GIVEN / WHEN — construction happens in setup_method

        # THEN
        assert self.mgr._is_initialized is False
        assert self.mgr._last_refresh_time == 0.0
        assert self.mgr._stale_timer is None
        assert set(self.mgr._state.keys()) == set(Zone)
        assert all(text == "" for text in self.mgr._state.values())
        assert self.mock_font.truetype.call_count == 2
