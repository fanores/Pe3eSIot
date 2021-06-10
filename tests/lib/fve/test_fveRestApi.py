# content of test_fveRestApi.py

import pytest
from unittest.mock import patch
from lib.fve.FveRestApi import FveRestApi
from lib.common.IotError import FveRestApiError, HttpClientError


class TestFveRestApi:

	def setup_method(self):
		class FakeHttpClient(object):
			times_get_request_called = 0
			url_called = ''
			response = 'response'

			def get_request(self, url):
				self.times_get_request_called += 1
				self.url_called = url

				return self.response

		class FakeHttpClientWithException(object):
			times_get_request_called = 0

			def get_request(self, url):
				self.times_get_request_called += 1
				raise HttpClientError('generic exception')

		self.fakeHttpClient = FakeHttpClient()
		self.fakeHttpClientWithException = FakeHttpClientWithException()

	def teardown_method(self):
		self.fakeHttpClient = ''

	def test_actual_measurement_called_successfully(self):
		with patch('lib.fve.FveRestApi.HttpClient') as mock_http_client:

			# GIVEN
			fve_url = 'http://1.1.1.1:1234/'
			fake_http_client = self.fakeHttpClient
			mock_http_client.return_value = fake_http_client

			# WHEN
			fve_rest_api = FveRestApi(fve_url)
			actual_response = fve_rest_api.get_actual_measurements()

			# THEN
			assert actual_response == 'response'
			assert self.fakeHttpClient.url_called == 'http://1.1.1.1:1234/' + FveRestApi.ACTUAL_MEASUREMENT_SUFFIX
			assert self.fakeHttpClient.times_get_request_called == 1

	def test_actual_measurement_raises_exception(self):
		with pytest.raises(FveRestApiError):
			with patch('lib.fve.FveRestApi.HttpClient') as mock_http_client:

				# GIVEN
				fve_url = 'http://1.1.1.1:1234/'
				fake_http_client = self.fakeHttpClientWithException
				mock_http_client.return_value = fake_http_client

				# WHEN
				fve_rest_api = FveRestApi(fve_url)
				actual_response = fve_rest_api.get_actual_measurements()

				# THEN
				assert self.fakeHttpClient.times_get_request_called == 1
				# FveRestApiError exception was raised

	def test_day_measurement_called_successfully(self):
		with patch('lib.fve.FveRestApi.HttpClient') as mock_http_client:

			# GIVEN
			fve_url = 'http://1.1.1.1:1234/'
			fake_http_client = self.fakeHttpClient
			mock_http_client.return_value = fake_http_client

			# WHEN
			fve_rest_api = FveRestApi(fve_url)
			actual_response = fve_rest_api.get_day_measurements('1')

			# THEN
			assert actual_response == 'response'
			expected_url_called = 'http://1.1.1.1:1234/' + 'stat_day.xml?day=1'
			assert self.fakeHttpClient.url_called == expected_url_called
			assert self.fakeHttpClient.times_get_request_called == 1

	def test_day_measurement_raises_exception(self):
		with pytest.raises(FveRestApiError):
			with patch('lib.fve.FveRestApi.HttpClient') as mock_http_client:

				# GIVEN
				fve_url = 'http://1.1.1.1:1234/'
				fake_http_client = self.fakeHttpClientWithException
				mock_http_client.return_value = fake_http_client

				# WHEN
				fve_rest_api = FveRestApi(fve_url)
				actual_response = fve_rest_api.get_day_measurements('1')

				# THEN
				assert self.fakeHttpClient.times_get_request_called == 1
				# FveRestApiError exception was raised
