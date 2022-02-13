# content of test_fveFileReporter.py

import pytest
from unittest.mock import patch
from lib.fve.FveFileReporter import FveFileReporter
from lib.common.IotError import FveFileReporterError, FileProcessorError


class TestFveFileReporter:

	def setup_method(self):
		class FakeFileProcessor(object):
			times_append_lines_called = 0
			line = ''

			def append_line_into_file(self, line):
				self.times_append_lines_called += 1
				self.line = line

		class FakeFileProcessorWithException(object):
			times_append_lines_called = 0

			def append_line_into_file(self, line):
				self.times_append_lines_called += 1
				raise FileProcessorError('File Processor exception')

		self.fakeFileProcessor = FakeFileProcessor()
		self.fakeFileProcessorException = FakeFileProcessorWithException()

	def teardown_method(self):
		self.fakeFileProcessor = ''
		self.fakeFileProcessorException = ''

	def test_write_measurements_to_file_with_all_kpis(self):
		with patch('lib.fve.FveFileReporter.FileProcessor') as mock_file_processor:

			# GIVEN
			file = ''
			kpis = ["E1", "E2", "E3"]
			measurements = {"E1": "today", "E2": "100", "E3": "dummyText"}
			fake_file_processor = self.fakeFileProcessor
			mock_file_processor.return_value = fake_file_processor

			# WHEN
			fve_file_reporter = FveFileReporter(file)
			fve_file_reporter.write_measurements_to_file(measurements, kpis)

			# THEN
			assert self.fakeFileProcessor.times_append_lines_called == 1
			assert self.fakeFileProcessor.line == "today;100;dummyText;"

	def test_write_measurements_to_file_with_partial_kpis(self):
		with patch('lib.fve.FveFileReporter.FileProcessor') as mock_file_processor:
			# GIVEN
			file = ''
			kpis = ["XX1", "E2", "XX3"]
			measurements = {"XX4": "today", "E2": "100", "E3": "dummyText"}
			fake_file_processor = self.fakeFileProcessor
			mock_file_processor.return_value = fake_file_processor

			# WHEN
			fve_file_reporter = FveFileReporter(file)
			fve_file_reporter.write_measurements_to_file(measurements, kpis)

			# THEN
			assert self.fakeFileProcessor.times_append_lines_called == 1
			assert self.fakeFileProcessor.line == "100;"

	def test_write_measurements_to_file_with_no_kpis(self):
		with patch('lib.fve.FveFileReporter.FileProcessor') as mock_file_processor:
			# GIVEN
			file = ''
			kpis = []
			measurements = {"E1": "with", "E2": "no", "E3": "kpis"}
			fake_file_processor = self.fakeFileProcessor
			mock_file_processor.return_value = fake_file_processor

			# WHEN
			fve_file_reporter = FveFileReporter(file)
			fve_file_reporter.write_measurements_to_file(measurements, kpis)

			# THEN
			assert self.fakeFileProcessor.times_append_lines_called == 0
			assert self.fakeFileProcessor.line == ""

	def test_write_measurements_to_file_raise_exception(self):
		with pytest.raises(FveFileReporterError):
			with patch('lib.fve.FveFileReporter.FileProcessor') as mock_file_processor:
				# GIVEN
				file = ''
				kpis = ["E1", "E2", "E3"]
				measurements = {"E1": "today", "E2": "100", "E3": "dummyText"}
				fake_file_processor = self.fakeFileProcessorException
				mock_file_processor.return_value = fake_file_processor

				# WHEN
				fve_file_reporter = FveFileReporter(file)
				fve_file_reporter.write_measurements_to_file(measurements, kpis)

				# THEN
				assert self.fakeFileProcessorException.times_append_lines_called == 1
				# FveFileReporterError exception was raised
