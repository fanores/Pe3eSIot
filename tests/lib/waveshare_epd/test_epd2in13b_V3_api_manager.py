import sys
import time
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

    # ------------------------------------------------------------------
    # sleep
    # ------------------------------------------------------------------

    def test_sleep_calls_epd_sleep(self):
        # GIVEN — display is initialized and a stale timer is running
        self.mgr._is_initialized = True
        self.mgr._stale_timer = MagicMock()

        # WHEN
        self.mgr.sleep()

        # THEN
        self.mock_epd.sleep.assert_called_once()
        assert self.mgr._is_initialized is False
        assert self.mgr._stale_timer is None

    # ------------------------------------------------------------------
    # set_zone
    # ------------------------------------------------------------------

    def test_set_zone_updates_state(self):
        # GIVEN
        zone = Zone.TOP_LEFT

        # WHEN
        self.mgr.set_zone(zone, "AB")

        # THEN
        assert self.mgr._state[zone] == "AB"
        self.mock_epd.display.assert_not_called()

    def test_set_zone_invalid_raises(self):
        # GIVEN
        invalid_zone = "not_a_zone"

        # WHEN / THEN
        import pytest
        with pytest.raises(EinkDisplayManagerError) as exc_info:
            self.mgr.set_zone(invalid_zone, "AB")

        assert "not_a_zone" in exc_info.value.message

    # ------------------------------------------------------------------
    # refresh
    # ------------------------------------------------------------------

    def test_refresh_calls_display(self):
        # GIVEN
        self.mgr._is_initialized = True
        mock_black = MagicMock()
        mock_red = MagicMock()
        assert self.mgr._stale_timer is None

        with patch.object(self.mgr, '_render_images', return_value=(mock_black, mock_red)), \
             patch.object(epd2in13b_V3_api_manager, 'threading'):
            # WHEN
            self.mgr.refresh()

        # THEN
        self.mock_epd.display.assert_called_once_with(
            self.mock_epd.getbuffer.return_value,
            self.mock_epd.getbuffer.return_value,
        )
        assert self.mgr._last_refresh_time != 0.0
        assert self.mgr._stale_timer is not None

    def test_refresh_before_init_raises(self):
        # GIVEN — display has never been initialized (default state from __init__)

        # WHEN / THEN
        import pytest
        with pytest.raises(EinkDisplayManagerError) as exc_info:
            self.mgr.refresh()

        assert "not initialized" in exc_info.value.message

    def test_refresh_rate_warning(self):
        # GIVEN — a refresh happened 10 s ago (within the 180 s threshold)
        self.mgr._is_initialized = True
        self.mgr._last_refresh_time = time.time() - 10

        with patch.object(self.mgr, '_render_images', return_value=(MagicMock(), MagicMock())), \
             patch.object(epd2in13b_V3_api_manager, 'threading'), \
             patch.object(epd2in13b_V3_api_manager, 'logger') as mock_logger:
            # WHEN
            self.mgr.refresh()

        # THEN — warning was logged and display was still called
        mock_logger.warning.assert_called_once()
        self.mock_epd.display.assert_called_once()

    def test_empty_zones_skipped_in_render(self):
        # GIVEN — all zones are empty (default state from __init__)

        with patch.object(epd2in13b_V3_api_manager, 'ImageDraw') as mock_image_draw:
            mock_draw = MagicMock()
            mock_image_draw.Draw.return_value = mock_draw

            # WHEN
            self.mgr._render_images()

        # THEN — draw.text was never called for any zone
        mock_draw.text.assert_not_called()

    def test_state_persists_across_refreshes(self):
        # GIVEN
        self.mgr._is_initialized = True
        self.mgr.set_zone(Zone.TOP_LEFT, "Hello")

        with patch.object(epd2in13b_V3_api_manager, 'ImageDraw') as mock_image_draw, \
             patch.object(epd2in13b_V3_api_manager, 'threading'), \
             patch.object(epd2in13b_V3_api_manager, 'logger'):
            mock_draw = MagicMock()
            mock_image_draw.Draw.return_value = mock_draw

            # WHEN — refresh twice
            self.mgr.refresh()
            self.mgr.refresh()

        # THEN — draw.text called once per refresh, proving state persisted
        assert mock_draw.text.call_count == 2
        assert self.mgr._state[Zone.TOP_LEFT] == "Hello"

    # ------------------------------------------------------------------
    # stale timer
    # ------------------------------------------------------------------

    def test_refresh_schedules_stale_timer(self):
        # GIVEN
        self.mgr._is_initialized = True

        with patch.object(self.mgr, '_render_images', return_value=(MagicMock(), MagicMock())), \
             patch.object(epd2in13b_V3_api_manager, 'threading') as mock_threading:
            # WHEN
            self.mgr.refresh()

        # THEN — a 24 h daemon timer targeting _force_refresh was created and started
        mock_threading.Timer.assert_called_once_with(86400, self.mgr._force_refresh)
        assert self.mgr._stale_timer.daemon is True
        self.mgr._stale_timer.start.assert_called_once()

    def test_refresh_reschedules_timer(self):
        # GIVEN
        self.mgr._is_initialized = True
        first_timer = MagicMock()
        second_timer = MagicMock()

        with patch.object(self.mgr, '_render_images', return_value=(MagicMock(), MagicMock())), \
             patch.object(epd2in13b_V3_api_manager, 'threading') as mock_threading, \
             patch.object(epd2in13b_V3_api_manager, 'logger'):
            # side_effect with a list returns a different mock on each Timer() call,
            # allowing us to assert on the first and second timer independently
            mock_threading.Timer.side_effect = [first_timer, second_timer]

            # WHEN — refresh twice
            self.mgr.refresh()
            self.mgr.refresh()

        # THEN — first timer was cancelled, second timer is now active
        first_timer.cancel.assert_called_once()
        second_timer.start.assert_called_once()
        assert self.mgr._stale_timer is second_timer

    # ------------------------------------------------------------------
    # _force_refresh
    # ------------------------------------------------------------------

    def test_force_refresh_calls_refresh_when_initialized(self):
        # GIVEN
        self.mgr._is_initialized = True

        with patch.object(self.mgr, 'refresh') as mock_refresh, \
             patch.object(epd2in13b_V3_api_manager, 'logger') as mock_logger:
            # WHEN
            self.mgr._force_refresh()

        # THEN
        mock_logger.warning.assert_called_once()
        mock_refresh.assert_called_once()
