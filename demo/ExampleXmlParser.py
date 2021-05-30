"""DEMO - XML Parser"""
from lib.common import HttpClient
from lib.common.IotError import HttpClientError
from lib.common import XmlParser
from lib.common.IotError import XmlParserError
from datetime import datetime


def main():
	# Initialization
	fve_url = 'http://192.168.2.51:8003/'

	# Trigger the processing
	process_actual_measurement(fve_url)


def process_actual_measurement(fve_url):
	print('Processing starts at: {}'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

	print('HTTP Client Processing:')
	ACTUAL_MEASUREMENT_URL_SUFFIX = 'meas.xml'
	request_url = fve_url + ACTUAL_MEASUREMENT_URL_SUFFIX
	http_client = HttpClient()
	try:
		fve_response = http_client.get_request(request_url)
	except HttpClientError as error:
		print(error)

	print('XML Processing:')
	xml_parser = XmlParser()
	try:
		elements = xml_parser.parse_root_child_elements_into_dictionary(fve_response.text)
	except XmlParserError as error:
		print(error)

	print(elements)

	print('Processing is finished!')


if __name__ == '__main__':
	main()
