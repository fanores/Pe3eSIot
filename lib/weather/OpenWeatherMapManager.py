"""Open Weather Map Manager"""
from pyowm import OWM
from lib.common.IotError import OwmManagerError


class OpenWeatherMapManager:

    # constructor
    def __init__(self, api_key):
        self.owm = OWM(api_key)
        self.owm_manager = self.owm.weather_manager()

    def get_current_temperature_at_place(self, city, country, unit="celsius"):
        """
            Get Current Temperature at Place: returns current temperature at place specified by city name and country
        :return: current temperature at place
        """
        place = city + ',' + country
        current_weather = self.owm_manager.weather_at_place(place).weather
        current_temperature = current_weather.temperature(unit)

        return current_temperature + unit
