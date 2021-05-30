# content of test_httpClient.py

import pytest
from unittest.mock import patch
from requests.exceptions import HTTPError
from lib.common.HttpClient import HttpClient
from lib.common.IotError import HttpClientError


class TestHttpClient:

    def test_response_called_successfully(self):
        with patch('requests.get') as mock_request:

            class FakeResponse(object):
                status_code = 200
                content = 'success'
                raise_for_status_has_no_error = False

                def raise_for_status(self):
                    self.raise_for_status_has_no_error = True

            # GIVEN
            called_url = 'http://myapi.com'
            fake_response = FakeResponse()
            mock_request.return_value = fake_response

            # WHEN
            http_client = HttpClient()
            actual_response = http_client.get_request(called_url)

            # THEN
            assert actual_response.status_code == 200
            assert actual_response.content == 'success'

    def test_response_called_successfully_with_url(self):
        with patch('requests.get') as mock_request:

            class FakeResponse(object):
                status_code = 200
                content = 'success'
                raise_for_status_has_no_error = False

                def raise_for_status(self):
                    self.raise_for_status_has_no_error = True

            # GIVEN
            called_url = 'http://myapi.com'
            fake_response = FakeResponse()
            mock_request.return_value = fake_response

            # WHEN
            http_client = HttpClient()
            http_client.get_request(called_url)

            # THEN
            mock_request.assert_called_once_with(called_url)

    def test_response_called_successfully_without_raising_exception(self):
        with patch('requests.get') as mock_request:

            class FakeResponse(object):
                status_code = 200
                content = 'success'
                raise_for_status_has_no_error = False

                def raise_for_status(self):
                    self.raise_for_status_has_no_error = True

            # GIVEN
            called_url = 'http://myapi.com'
            fake_response = FakeResponse()
            mock_request.return_value = fake_response

            # WHEN
            http_client = HttpClient()
            actual_response = http_client.get_request(called_url)

            # THEN
            assert actual_response.raise_for_status_has_no_error is True

    def test_response_raises_exception_on_http_error(self):
        with pytest.raises(HttpClientError, match=r'.* HTTPError .*'):
            with patch('requests.get') as mock_request:
                class FakeResponse(object):
                    status_code = 200
                    content = 'success'
                    raise_for_status_has_no_error = False

                    def raise_for_status(self):
                        self.raise_for_status_has_no_error = False
                        raise HTTPError('HTTPError raised')

                # GIVEN
                called_url = 'http://myapi.com'
                fake_response = FakeResponse()
                mock_request.return_value = fake_response

                # WHEN
                http_client = HttpClient()
                http_client.get_request(called_url)

                # THEN
                # HttpClientError exception was raised

    def test_response_raises_exception_on_exception(self):
        with pytest.raises(HttpClientError, match=r'.* ExceptionError .*'):
            with patch('requests.get') as mock_request:
                class FakeResponse(object):
                    status_code = 200
                    content = 'success'
                    raise_for_status_has_no_error = False

                    def raise_for_status(self):
                        self.raise_for_status_has_no_error = False
                        raise Exception('ExceptionError raised')

                # GIVEN
                called_url = 'http://myapi.com'
                fake_response = FakeResponse()
                mock_request.return_value = fake_response

                # WHEN
                http_client = HttpClient()
                http_client.get_request(called_url)

                # THEN
                # HttpClientError exception was raised
