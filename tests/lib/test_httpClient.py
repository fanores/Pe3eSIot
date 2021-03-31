# content of test_httpClient.py

from unittest.mock import patch
from lib.HttpClient import HttpClient


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
            actual_response = HttpClient.get_request(called_url)

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
            actual_response = HttpClient.get_request(called_url)

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
            actual_response = HttpClient.get_request(called_url)

            # THEN
            assert actual_response.raise_for_status_has_no_error is True
