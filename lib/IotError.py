"""IoT Error/Exception"""


class IotError(Exception):
	"""Base class for exceptions in IoT project."""
	pass


class HttpClientError(IotError):
	"""Exceptions raised for HTTP errors."""

	def __init__(self, message):
		self.message = message
