"""HTTP Client"""
import requests
from requests.exceptions import HTTPError
from lib.IotError import HttpClientError


class HttpClient:
    @staticmethod
    def get_request(url):
        """
            Get Request: returns the response of the request call
        :return: request response
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
        except HTTPError as http_error:
            raise HttpClientError('Request error: {}'.format(print(http_error)))
        except Exception as error:
            raise HttpClientError('Request error: {}'.format(print(error)))

        return response
