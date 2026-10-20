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

    # ------------------------------------------------------------------
    # init
    # ------------------------------------------------------------------

    def test_init_success(self):
        # GIVEN
        self.mock_epd.init.return_value = 0

        # WHEN
        self.mgr.init()

        # THEN
        self.mock_epd.init.assert_called_once()
        assert self.mgr._is_initialized is True

    def test_init_failure(self):
        # GIVEN
        self.mock_epd.init.return_value = -1

        # WHEN / THEN
        import pytest
        with pytest.raises(EinkDisplayManagerError) as exc_info:
            self.mgr.init()

        assert exc_info.value.message == "EPD init failed with code -1"
        assert self.mgr._is_initialized is False

    # ------------------------------------------------------------------
    # clear
    # ------------------------------------------------------------------

    def test_clear_calls_epd_clear(self):
        # GIVEN — some zones have text
        self.mgr._state[Zone.TOP_LEFT] = "Hello"
        self.mgr._state[Zone.MIDDLE_CENTER] = "World"

        # WHEN
        self.mgr.clear()

        # THEN
        self.mock_epd.Clear.assert_called_once()
        assert all(text == "" for text in self.mgr._state.values())
