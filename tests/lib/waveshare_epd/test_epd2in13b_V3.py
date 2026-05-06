# content of test_epd2in13b_V3.py

import sys
from unittest.mock import MagicMock, call

# Inject the hardware shim into sys.modules before importing the module under test,
# because epdconfig is a non-existent hardware module loaded at package import time.
mock_epdconfig = MagicMock()
mock_epdconfig.RST_PIN = 11
mock_epdconfig.DC_PIN = 25
mock_epdconfig.BUSY_PIN = 24
mock_epdconfig.CS_PIN = 8
sys.modules['lib.waveshare_epd.epdconfig'] = mock_epdconfig

from lib.waveshare_epd.epd2in13b_V3 import EPD, EPD_WIDTH, EPD_HEIGHT  # noqa: E402

from PIL import Image  # noqa: E402


class TestEPD:

    def setup_method(self):
        # Reset all call records AND side_effects so nothing bleeds between tests.
        mock_epdconfig.reset_mock(side_effect=True)
        # Restore pin constants after reset_mock clears them.
        mock_epdconfig.RST_PIN = 11
        mock_epdconfig.DC_PIN = 25
        mock_epdconfig.BUSY_PIN = 24
        mock_epdconfig.CS_PIN = 8
        # Default: module_init succeeds and digital_read immediately non-zero
        # (so ReadBusy exits after the first check without looping).
        mock_epdconfig.module_init.return_value = 0
        mock_epdconfig.digital_read.return_value = 1
        self.epd = EPD()

    def teardown_method(self):
        self.epd = None

    # ------------------------------------------------------------------
    # __init__
    # ------------------------------------------------------------------

    def test_init_assigns_pins(self):
        # GIVEN / WHEN
        epd = EPD()

        # THEN
        assert epd.reset_pin == 11
        assert epd.dc_pin == 25
        assert epd.busy_pin == 24
        assert epd.cs_pin == 8

    def test_init_assigns_dimensions(self):
        # GIVEN / WHEN
        epd = EPD()

        # THEN
        assert epd.width == EPD_WIDTH
        assert epd.height == EPD_HEIGHT
        assert epd.width == 104
        assert epd.height == 212

    # ------------------------------------------------------------------
    # reset
    # ------------------------------------------------------------------

    def test_reset_calls_digital_write_three_times_with_reset_pin(self):
        # GIVEN
        epd = self.epd

        # WHEN
        epd.reset()

        # THEN — digital_write must be called exactly 3 times with the reset pin
        digital_write_calls = mock_epdconfig.digital_write.call_args_list
        reset_pin_calls = [c for c in digital_write_calls if c.args[0] == epd.reset_pin]
        assert len(reset_pin_calls) == 3

    def test_reset_drives_pin_high_low_high(self):
        # GIVEN
        epd = self.epd

        # WHEN
        epd.reset()

        # THEN — the sequence of values written to the reset pin is 1, 0, 1
        digital_write_calls = mock_epdconfig.digital_write.call_args_list
        reset_pin_calls = [c for c in digital_write_calls if c.args[0] == epd.reset_pin]
        values = [c.args[1] for c in reset_pin_calls]
        assert values == [1, 0, 1]

    def test_reset_calls_delay_ms_three_times(self):
        # GIVEN
        epd = self.epd

        # WHEN
        epd.reset()

        # THEN
        assert mock_epdconfig.delay_ms.call_count == 3

    # ------------------------------------------------------------------
    # send_command
    # ------------------------------------------------------------------

    def test_send_command_sets_dc_low_then_cs_low_high(self):
        # GIVEN
        epd = self.epd

        # WHEN
        epd.send_command(0xAB)

        # THEN — dc must be set to 0, cs toggled 0→1 around the SPI write
        digital_write_calls = mock_epdconfig.digital_write.call_args_list
        assert call(epd.dc_pin, 0) in digital_write_calls
        assert call(epd.cs_pin, 0) in digital_write_calls
        assert call(epd.cs_pin, 1) in digital_write_calls

    def test_send_command_writes_command_byte_via_spi(self):
        # GIVEN
        epd = self.epd

        # WHEN
        epd.send_command(0xAB)

        # THEN
        mock_epdconfig.spi_writebyte.assert_called_once_with([0xAB])

    def test_send_command_cs_is_deasserted_after_spi_write(self):
        # GIVEN
        epd = self.epd
        call_order = []
        mock_epdconfig.spi_writebyte.side_effect = lambda _: call_order.append('spi')
        mock_epdconfig.digital_write.side_effect = lambda pin, val: call_order.append(('dw', pin, val))

        # WHEN
        epd.send_command(0xAB)

        # THEN — CS=1 must follow the SPI write
        spi_idx = call_order.index('spi')
        cs_high_idx = call_order.index(('dw', epd.cs_pin, 1))
        assert cs_high_idx > spi_idx

    # ------------------------------------------------------------------
    # send_data
    # ------------------------------------------------------------------

    def test_send_data_sets_dc_high(self):
        # GIVEN
        epd = self.epd

        # WHEN
        epd.send_data(0x77)

        # THEN — dc must be 1 for data (versus 0 for command)
        assert call(epd.dc_pin, 1) in mock_epdconfig.digital_write.call_args_list

    def test_send_data_toggles_cs_around_spi_write(self):
        # GIVEN
        epd = self.epd

        # WHEN
        epd.send_data(0x77)

        # THEN
        assert call(epd.cs_pin, 0) in mock_epdconfig.digital_write.call_args_list
        assert call(epd.cs_pin, 1) in mock_epdconfig.digital_write.call_args_list

    def test_send_data_writes_data_byte_via_spi(self):
        # GIVEN
        epd = self.epd

        # WHEN
        epd.send_data(0x77)

        # THEN
        mock_epdconfig.spi_writebyte.assert_called_once_with([0x77])

    # ------------------------------------------------------------------
    # ReadBusy
    # ------------------------------------------------------------------

    def test_readbusy_sends_0x71_before_polling(self):
        # GIVEN — digital_read returns 1 immediately (not busy)
        mock_epdconfig.digital_read.return_value = 1
        epd = self.epd

        # WHEN
        epd.ReadBusy()

        # THEN — 0x71 was sent via send_command at least once
        spi_calls = mock_epdconfig.spi_writebyte.call_args_list
        assert call([0x71]) in spi_calls

    def test_readbusy_loops_until_digital_read_nonzero(self):
        # GIVEN — busy (0) twice, then ready (1)
        mock_epdconfig.digital_read.side_effect = [0, 0, 1]
        epd = self.epd

        # WHEN
        epd.ReadBusy()

        # THEN — digital_read called 3 times total
        assert mock_epdconfig.digital_read.call_count == 3

    def test_readbusy_calls_delay_ms_while_looping(self):
        # GIVEN — busy once, then ready
        mock_epdconfig.digital_read.side_effect = [0, 1]
        epd = self.epd

        # WHEN
        epd.ReadBusy()

        # THEN — delay_ms called at least once (inside the loop)
        assert mock_epdconfig.delay_ms.call_count >= 1

    def test_readbusy_resends_0x71_each_loop_iteration(self):
        # GIVEN — busy once, then ready (so the loop body runs once)
        mock_epdconfig.digital_read.side_effect = [0, 1]
        epd = self.epd

        # WHEN
        epd.ReadBusy()

        # THEN — 0x71 is sent as the initial call and once more inside the loop
        spi_calls = mock_epdconfig.spi_writebyte.call_args_list
        cmd_71_calls = [c for c in spi_calls if c == call([0x71])]
        assert len(cmd_71_calls) >= 2

    # ------------------------------------------------------------------
    # init
    # ------------------------------------------------------------------

    def test_init_returns_minus_one_when_module_init_fails(self):
        # GIVEN
        mock_epdconfig.module_init.return_value = 1
        epd = self.epd

        # WHEN
        result = epd.init()

        # THEN
        assert result == -1

    def test_init_returns_zero_on_success(self):
        # GIVEN
        mock_epdconfig.module_init.return_value = 0
        mock_epdconfig.digital_read.return_value = 1
        epd = self.epd

        # WHEN
        result = epd.init()

        # THEN
        assert result == 0

    def test_init_does_not_call_reset_when_module_init_fails(self):
        # GIVEN
        mock_epdconfig.module_init.return_value = 1
        epd = self.epd

        # WHEN
        epd.init()

        # THEN — no hardware interaction should have occurred
        mock_epdconfig.digital_write.assert_not_called()

    def test_init_calls_reset_on_success(self):
        # GIVEN
        mock_epdconfig.module_init.return_value = 0
        mock_epdconfig.digital_read.return_value = 1
        epd = self.epd

        # WHEN
        epd.init()

        # THEN — reset toggles the reset_pin (1, 0, 1)
        digital_write_calls = mock_epdconfig.digital_write.call_args_list
        reset_pin_calls = [c for c in digital_write_calls if c.args[0] == epd.reset_pin]
        assert len(reset_pin_calls) == 3

    def test_init_sends_panel_setting_command_sequence(self):
        # GIVEN
        mock_epdconfig.module_init.return_value = 0
        mock_epdconfig.digital_read.return_value = 1
        epd = self.epd

        # WHEN
        epd.init()

        # THEN — all expected command bytes are sent via spi_writebyte
        spi_calls = mock_epdconfig.spi_writebyte.call_args_list
        commands_sent = [c.args[0][0] for c in spi_calls]
        for expected_cmd in [0x04, 0x00, 0x61, 0x50]:
            assert expected_cmd in commands_sent

    # ------------------------------------------------------------------
    # getbuffer — vertical path (image matches width x height)
    # ------------------------------------------------------------------

    def test_getbuffer_vertical_all_white_returns_all_0xff(self):
        # GIVEN — a fully white image (PIL '1' mode: pixel value 255 = white)
        image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)
        epd = self.epd

        # WHEN
        buf = epd.getbuffer(image)

        # THEN — every byte is 0xFF (no bits cleared)
        assert all(b == 0xFF for b in buf)

    def test_getbuffer_vertical_black_pixel_at_origin_clears_msb_of_first_byte(self):
        # GIVEN — white image with a single black pixel at (0, 0)
        image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)
        image.putpixel((0, 0), 0)
        epd = self.epd

        # WHEN
        buf = epd.getbuffer(image)

        # THEN — pixel (0,0) maps to byte index 0; bit 7 (MSB) is cleared
        # buf[int((0 + 0*104)/8)] &= ~(0x80 >> (0 % 8))  →  buf[0] &= ~0x80  →  0x7F
        assert buf[0] == 0x7F

    def test_getbuffer_vertical_black_pixel_at_column_8_clears_msb_of_second_byte(self):
        # GIVEN — white image with a single black pixel at (8, 0)
        image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)
        image.putpixel((8, 0), 0)
        epd = self.epd

        # WHEN
        buf = epd.getbuffer(image)

        # THEN — pixel (8,0) maps to byte index int((8 + 0*104)/8) = 1; bit 7 cleared
        assert buf[1] == 0x7F
        assert buf[0] == 0xFF  # neighbouring byte untouched

    def test_getbuffer_vertical_black_pixel_at_column_1_clears_second_msb(self):
        # GIVEN — white image with a single black pixel at (1, 0)
        image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)
        image.putpixel((1, 0), 0)
        epd = self.epd

        # WHEN
        buf = epd.getbuffer(image)

        # THEN — pixel (1,0): byte index 0, bit mask ~(0x80>>1) = ~0x40 = 0xBF
        assert buf[0] == 0xBF

    def test_getbuffer_vertical_buffer_length_is_correct(self):
        # GIVEN
        image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)
        epd = self.epd

        # WHEN
        buf = epd.getbuffer(image)

        # THEN — expected buffer size: (width/8) * height = 13 * 212 = 2756
        assert len(buf) == (EPD_WIDTH // 8) * EPD_HEIGHT

    # ------------------------------------------------------------------
    # getbuffer — horizontal path (image is height x width, rotated)
    # ------------------------------------------------------------------

    def test_getbuffer_horizontal_all_white_returns_all_0xff(self):
        # GIVEN — fully white landscape image
        image = Image.new('1', (EPD_HEIGHT, EPD_WIDTH), 255)
        epd = self.epd

        # WHEN
        buf = epd.getbuffer(image)

        # THEN
        assert all(b == 0xFF for b in buf)

    def test_getbuffer_horizontal_black_pixel_at_origin_clears_correct_bit(self):
        # GIVEN — white landscape image with black pixel at (0, 0)
        image = Image.new('1', (EPD_HEIGHT, EPD_WIDTH), 255)
        image.putpixel((0, 0), 0)
        epd = self.epd

        # WHEN
        buf = epd.getbuffer(image)

        # THEN — rotation: newx = y = 0, newy = height - x - 1 = 212 - 0 - 1 = 211
        # byte index = int((0 + 211*104)/8) = int(21944/8) = 2743
        # bit mask = ~(0x80 >> (y % 8)) = ~(0x80 >> 0) = ~0x80 = 0x7F
        expected_byte_index = int((0 + 211 * EPD_WIDTH) / 8)
        assert buf[expected_byte_index] == 0x7F

    def test_getbuffer_horizontal_buffer_length_is_correct(self):
        # GIVEN
        image = Image.new('1', (EPD_HEIGHT, EPD_WIDTH), 255)
        epd = self.epd

        # WHEN
        buf = epd.getbuffer(image)

        # THEN
        assert len(buf) == (EPD_WIDTH // 8) * EPD_HEIGHT

    # ------------------------------------------------------------------
    # display
    # ------------------------------------------------------------------

    def test_display_sends_0x10_before_black_data(self):
        # GIVEN
        n = (EPD_WIDTH * EPD_HEIGHT) // 8
        imageblack = [0xAA] * n
        imagered = [0x55] * n
        epd = self.epd

        # WHEN
        epd.display(imageblack, imagered)

        # THEN — 0x10 appears in SPI calls
        spi_calls = mock_epdconfig.spi_writebyte.call_args_list
        assert call([0x10]) in spi_calls

    def test_display_sends_0x13_before_red_data(self):
        # GIVEN
        n = (EPD_WIDTH * EPD_HEIGHT) // 8
        imageblack = [0xAA] * n
        imagered = [0x55] * n
        epd = self.epd

        # WHEN
        epd.display(imageblack, imagered)

        # THEN
        spi_calls = mock_epdconfig.spi_writebyte.call_args_list
        assert call([0x13]) in spi_calls

    def test_display_sends_all_black_bytes(self):
        # GIVEN
        n = (EPD_WIDTH * EPD_HEIGHT) // 8
        imageblack = [0xAA] * n
        imagered = [0x55] * n
        epd = self.epd

        # WHEN
        epd.display(imageblack, imagered)

        # THEN — every black pixel byte is forwarded
        spi_calls = mock_epdconfig.spi_writebyte.call_args_list
        data_calls = [c.args[0][0] for c in spi_calls]
        assert data_calls.count(0xAA) == n

    def test_display_sends_all_red_bytes(self):
        # GIVEN
        n = (EPD_WIDTH * EPD_HEIGHT) // 8
        imageblack = [0xAA] * n
        imagered = [0x55] * n
        epd = self.epd

        # WHEN
        epd.display(imageblack, imagered)

        # THEN
        spi_calls = mock_epdconfig.spi_writebyte.call_args_list
        data_calls = [c.args[0][0] for c in spi_calls]
        assert data_calls.count(0x55) == n

    def test_display_sends_0x12_refresh_command(self):
        # GIVEN
        n = (EPD_WIDTH * EPD_HEIGHT) // 8
        imageblack = [0xFF] * n
        imagered = [0xFF] * n
        epd = self.epd

        # WHEN
        epd.display(imageblack, imagered)

        # THEN
        spi_calls = mock_epdconfig.spi_writebyte.call_args_list
        assert call([0x12]) in spi_calls

    def test_display_calls_delay_ms_before_readbusy(self):
        # GIVEN
        n = (EPD_WIDTH * EPD_HEIGHT) // 8
        imageblack = [0xFF] * n
        imagered = [0xFF] * n
        mock_epdconfig.digital_read.return_value = 1
        epd = self.epd

        # WHEN
        epd.display(imageblack, imagered)

        # THEN
        mock_epdconfig.delay_ms.assert_called()

    # ------------------------------------------------------------------
    # Clear
    # ------------------------------------------------------------------

    def test_clear_sends_0x10_command(self):
        # GIVEN
        mock_epdconfig.digital_read.return_value = 1
        epd = self.epd

        # WHEN
        epd.Clear()

        # THEN
        spi_calls = mock_epdconfig.spi_writebyte.call_args_list
        assert call([0x10]) in spi_calls

    def test_clear_sends_0x13_command(self):
        # GIVEN
        mock_epdconfig.digital_read.return_value = 1
        epd = self.epd

        # WHEN
        epd.Clear()

        # THEN
        spi_calls = mock_epdconfig.spi_writebyte.call_args_list
        assert call([0x13]) in spi_calls

    def test_clear_sends_0xff_for_all_black_pixels(self):
        # GIVEN
        mock_epdconfig.digital_read.return_value = 1
        epd = self.epd
        n = (EPD_WIDTH * EPD_HEIGHT) // 8

        # WHEN
        epd.Clear()

        # THEN — 0xFF is sent n times for the black plane and n times for the red plane
        spi_calls = mock_epdconfig.spi_writebyte.call_args_list
        ff_count = sum(1 for c in spi_calls if c == call([0xFF]))
        assert ff_count == n * 2

    def test_clear_sends_0x12_refresh_command(self):
        # GIVEN
        mock_epdconfig.digital_read.return_value = 1
        epd = self.epd

        # WHEN
        epd.Clear()

        # THEN
        spi_calls = mock_epdconfig.spi_writebyte.call_args_list
        assert call([0x12]) in spi_calls

    def test_clear_calls_delay_ms(self):
        # GIVEN
        mock_epdconfig.digital_read.return_value = 1
        epd = self.epd

        # WHEN
        epd.Clear()

        # THEN
        mock_epdconfig.delay_ms.assert_called()

    # ------------------------------------------------------------------
    # sleep
    # ------------------------------------------------------------------

    def test_sleep_sends_0x50_and_0xf7(self):
        # GIVEN
        mock_epdconfig.digital_read.return_value = 1
        epd = self.epd

        # WHEN
        epd.sleep()

        # THEN
        spi_calls = mock_epdconfig.spi_writebyte.call_args_list
        assert call([0x50]) in spi_calls
        assert call([0xf7]) in spi_calls

    def test_sleep_sends_0x02_for_power_off(self):
        # GIVEN
        mock_epdconfig.digital_read.return_value = 1
        epd = self.epd

        # WHEN
        epd.sleep()

        # THEN
        spi_calls = mock_epdconfig.spi_writebyte.call_args_list
        assert call([0x02]) in spi_calls

    def test_sleep_sends_deep_sleep_command_0x07_and_check_code_0xa5(self):
        # GIVEN
        mock_epdconfig.digital_read.return_value = 1
        epd = self.epd

        # WHEN
        epd.sleep()

        # THEN
        spi_calls = mock_epdconfig.spi_writebyte.call_args_list
        assert call([0x07]) in spi_calls
        assert call([0xA5]) in spi_calls

    def test_sleep_calls_delay_ms_2000(self):
        # GIVEN
        mock_epdconfig.digital_read.return_value = 1
        epd = self.epd

        # WHEN
        epd.sleep()

        # THEN — the 2000 ms power-down delay must be present
        assert call(2000) in mock_epdconfig.delay_ms.call_args_list

    def test_sleep_calls_module_exit(self):
        # GIVEN
        mock_epdconfig.digital_read.return_value = 1
        epd = self.epd

        # WHEN
        epd.sleep()

        # THEN
        mock_epdconfig.module_exit.assert_called_once()

    def test_sleep_module_exit_called_after_delay(self):
        # GIVEN
        mock_epdconfig.digital_read.return_value = 1
        epd = self.epd
        call_order = []
        mock_epdconfig.delay_ms.side_effect = lambda ms: call_order.append(('delay', ms))
        mock_epdconfig.module_exit.side_effect = lambda: call_order.append('module_exit')

        # WHEN
        epd.sleep()

        # THEN — the 2000 ms delay must precede module_exit
        delay_2000_idx = next(i for i, c in enumerate(call_order) if c == ('delay', 2000))
        module_exit_idx = call_order.index('module_exit')
        assert module_exit_idx > delay_2000_idx
