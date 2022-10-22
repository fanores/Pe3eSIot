import pytest
from unittest.mock import patch, Mock, call
from lib.weather.OpenWeatherMapManager import OpenWeatherMapManager
from lib.common.IotError import OwmManagerError


class FakeWeather(object):

	def temperature(self, unit):
		return '9'


class FakeWeatherManager(object):

	def __init__(self, raise_owm_manager_exception):
		self.place = ''
		self.weather = ''
		self.raise_exception = raise_owm_manager_exception

	def weather_at_place(self, place):
		if self.raise_exception:
			raise Exception('Error in OWM')

		self.place = place
		self.weather = FakeWeather()
		return self


class FakeOwm(object):

	def __init__(self, api_key, raise_owm_manager_exception):
		self.api_key = api_key
		self.weather_manager_called = False
		self.raise_owm_manager_exception = raise_owm_manager_exception

	def weather_manager(self):
		self.weather_manager_called = True
		return FakeWeatherManager(self.raise_owm_manager_exception)


def mock_owm(api_key, raise_owm_manager_exception=False):
	return FakeOwm(api_key, raise_owm_manager_exception)


class TestOpenWeatherMapManager:

	@patch('lib.weather.OpenWeatherMapManager.OWM')
	def test_create_open_weather_map_manager(self, owm_patch):
		# GIVEN
		fake_api_key = '1234'
		owm_patch.return_value = mock_owm(fake_api_key)

		# WHEN
		owm_manager = OpenWeatherMapManager(fake_api_key)

		# THEN
		assert owm_manager.owm.api_key == '1234'
		assert owm_manager.owm.weather_manager_called

	@patch('lib.weather.OpenWeatherMapManager.OWM')
	def test_get_current_temperature_at_place_with_default_units_successfully(self, owm_patch):
		# GIVEN
		fake_api_key = '1234'
		owm_patch.return_value = mock_owm(fake_api_key)

		# WHEN
		owm_manager = OpenWeatherMapManager(fake_api_key)
		current_temperature = owm_manager.get_current_temperature_at_place('Nemsova', 'SK')

		# THEN
		assert current_temperature == '9celsius'

	@patch('lib.weather.OpenWeatherMapManager.OWM')
	def test_get_current_temperature_at_place_with_exact_units_successfully(self, owm_patch):
		# GIVEN
		fake_api_key = '1234'
		owm_patch.return_value = mock_owm(fake_api_key)

		# WHEN
		owm_manager = OpenWeatherMapManager(fake_api_key)
		current_temperature = owm_manager.get_current_temperature_at_place('Nemsova', 'SK', 'farenheit')

		# THEN
		assert current_temperature == '9farenheit'

	@patch('lib.weather.OpenWeatherMapManager.OWM')
	def test_create_open_weather_map_manager_exception(self, owm_patch):
		with pytest.raises(OwmManagerError, match=r'.*OWM Error.*'):
			# GIVEN
			fake_api_key = None
			owm_patch.side_effect = AssertionError('Error in OWM')

			# WHEN
			owm_manager = OpenWeatherMapManager(fake_api_key)

	@patch('lib.weather.OpenWeatherMapManager.OWM')
	def test_get_current_temperature_at_place_exception(self, owm_patch):
		with pytest.raises(OwmManagerError, match=r'.*OWM Error.*'):
			# GIVEN
			fake_api_key = '1234'
			raise_weather_manager_exception = True
			owm_patch.return_value = mock_owm(fake_api_key, raise_weather_manager_exception)

			# WHEN
			owm_manager = OpenWeatherMapManager(fake_api_key)
			current_temperature = owm_manager.get_current_temperature_at_place('Nemsova', 'SK')
