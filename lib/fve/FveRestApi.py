"""Fve Rest Api"""
from lib.common.HttpClient import HttpClient
from lib.common.IotError import HttpClientError
from lib.common.IotError import FveRestApiError


class FveRestApi:
	# constants
	ACTUAL_MEASUREMENT_SUFFIX = 'meas.xml'
	DAY_MEASUREMENT_SUFFIX = 'stat_day.xml?day={index}'

	# constructor
	def __init__(self, fve_url):
		self.url = fve_url
		self.http_client = HttpClient()

	# retrieve FVE day measurements
	def get_day_measurements(self, day_index):
		"""
			Retrieve measurements of a selected day.
			Day Measurements URL: 'http://1.1.1.1:port/stat_day.xml?day={index}'
			Day Index: 	1: yesterday
						2: day before yesterday
						...
		return: request response
		"""
		request_url = self.url + self.DAY_MEASUREMENT_SUFFIX
		request_url = request_url.replace('{index}', day_index)

		try:
			response = self.http_client.get_request(request_url)
		except HttpClientError as error:
			raise FveRestApiError(error.message)

	# retrieve FVE actual measurements
	def get_actual_measurements(self):
		"""
			Retrieve actual measurements.
			Actual Measurements URL: 'http://1.1.1.1:port/meas.xml'
		: return: request response
		"""
		request_url = self.url + self.ACTUAL_MEASUREMENT_SUFFIX

		try:
			response = self.http_client.get_request(request_url)
		except HttpClientError as error:
			raise FveRestApiError(error.message)

		return response
