"""Open Weather Map Manager"""
from pyowm import OWM
from lib.common.IotError import OwmManagerError


class OpenWeatherMapManager:

    # constructor
    def __init__(self, api_key):
        self.owm = OWM(api_key)
        self.owm_manager = self.owm.weather_manager()

    def get_city_id_by_city_name(self, city, country):
        """
            Get City ID: returns the city ID from city name and country
        :return: city id
        """
        registry = self.owm.city_id_registry()
        city_list = registry.ids_for(city, country, matching='exact')
        city_properties = city_list[0]

        return city_properties[0]

    def get_geo_location_by_city_name(self, city, country):
        """
            Get City Geo Locations: returns the city GEO Location coordinates
        :return: geo location coordinates
        """
        registry = self.owm.city_id_registry()
        city_list = registry.locations_for(city, country, matching='exact')
        city_geo_coordinates = city_list[0]

        return city_geo_coordinates

    def get_current_temperature_at_place(self, city, country, unit="celsius"):
        """
            Get Current Temperature at Place: returns current temperature at place specified by city name and country
        :return: current temperature at place
        """
        place = city + ',' + country
        current_weather = self.owm_manager.weather_at_place(place).weather
        current_temperature = current_weather.temperature(unit)

        return current_temperature + unit
