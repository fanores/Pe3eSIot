"""HTTP Client"""
import requests
from requests.exceptions import HTTPError
from lib.common.IotError import HttpClientError


class HttpClient:

    def get_request(self, url):
        """
            Get Request: returns the response of the request call
        :return: request response
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
        except HTTPError as http_error:
            raise HttpClientError('Get request error: {}'.format(http_error))
        except Exception as error:
            raise HttpClientError('Get request error: {}'.format(error))

        return response
