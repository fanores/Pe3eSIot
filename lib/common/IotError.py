"""IoT Error/Exception"""


class IotError(Exception):
	"""Base class for exceptions in IoT project."""
	pass


class HttpClientError(IotError):
	"""Exceptions raised for HTTP errors."""

	def __init__(self, message):
		self.message = message


class XmlParserError(IotError):
	"""Exceptions raised for XML parsing errors."""

	def __init__(self, message):
		self.message = message


class FileProcessorError(IotError):
	"""Exceptions raised for File processing errors."""

	def __init__(self, message):
		self.message = message

class FveRestApiError(IotError):
	"""Exceptions raised for FVE REST API"""

	def __init__(self, message):
		self.message = message
