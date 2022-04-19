import pytest
from datetime import datetime
from lib.common.DateTimeProcessor import DateTimeProcessor


class TestDateTime:

	def test_get_date_with_default_delimiter(self):
		# GIVEN
		mocked_now = datetime(2022, 4, 9, 21, 43, 21)

		# WHEN
		date_time_processor = DateTimeProcessor(mocked_now)
		date_as_string = date_time_processor.get_date()

		# THEN
		assert date_as_string == '9.4.2022'

	def test_get_date_with_custom_delimiter(self):
		# GIVEN
		mocked_now = datetime(2022, 4, 9, 21, 43, 21)

		# WHEN
		date_time_processor = DateTimeProcessor(mocked_now)
		date_as_string = date_time_processor.get_date('/')

		# THEN
		assert date_as_string == '9/4/2022'

	def test_get_time_with_seconds(self):
		# GIVEN
		mocked_now = datetime(2022, 4, 9, 6, 3, 21)

		# WHEN
		date_time_processor = DateTimeProcessor(mocked_now)
		time_as_string = date_time_processor.get_time()

		# THEN
		assert time_as_string == '6:3:21'

	def test_get_time_without_seconds(self):
		# GIVEN
		mocked_now = datetime(2022, 4, 9, 6, 3, 21)

		# WHEN
		date_time_processor = DateTimeProcessor(mocked_now)
		time_as_string = date_time_processor.get_time(False)

		# THEN
		assert time_as_string == '6:3'

	def test_set_date_time(self):
		# GIVEN
		mocked_constructor_now = datetime(2022, 4, 9, 21, 43, 21)
		mocked_set_now = datetime(2022, 11, 11, 19, 12, 21)

		# WHEN
		date_time_processor = DateTimeProcessor(mocked_constructor_now)
		date_time_processor.set_date_time(mocked_set_now)

		# THEN
		assert date_time_processor.now == mocked_set_now

	def test_get_full_weekday_name(self):
		# GIVEN
		mocked_now = datetime(2022, 4, 9, 6, 3, 21)

		# WHEN
		date_time_processor = DateTimeProcessor(mocked_now)
		full_weekday_name = date_time_processor.get_full_weekday_name()

		# THEN
		assert full_weekday_name == 'Saturday'

	def test_get_abbreviated_weekday_name(self):
		# GIVEN
		mocked_now = datetime(2022, 4, 10, 6, 3, 21)

		# WHEN
		date_time_processor = DateTimeProcessor(mocked_now)
		abbreviated_weekday_name = date_time_processor.get_abbreviated_weekday_name()

		# THEN
		assert abbreviated_weekday_name == 'Sun'

	def test_get_full_month_name(self):
		# GIVEN
		mocked_now = datetime(2022, 12, 9, 6, 3, 21)

		# WHEN
		date_time_processor = DateTimeProcessor(mocked_now)
		full_month_name = date_time_processor.get_full_month_name()

		# THEN
		assert full_month_name == 'December'

	def test_get_abbreviated_month_name(self):
		# GIVEN
		mocked_now = datetime(2022, 10, 9, 6, 3, 21)

		# WHEN
		date_time_processor = DateTimeProcessor(mocked_now)
		full_abbreviated_name = date_time_processor.get_abbreviated_month_name()

		# THEN
		assert full_abbreviated_name == 'Oct'
