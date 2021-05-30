import pytest
from unittest.mock import patch, mock_open
from lib.common.FileProcessor import FileProcessor
from lib.common.IotError import FileProcessorError


class TestFileProcessor:

	def test_write_into_file_successfully(self):
		with patch('builtins.open', mock_open()) as mocked_file:
			# GIVEN
			file_path = 'fake/file/path'
			content = 'My file content'

			# WHEN
			file_processor = FileProcessor(file_path)
			file_processor.append_line_into_file(content)

			# THEN
			mocked_file.assert_called_once_with(file_path, 'a+')
			mocked_file().write.assert_called_once_with(content + '\n')

	def test_write_into_file_raises_exception(self):
		with pytest.raises(FileProcessorError):
			with patch('builtins.open', mock_open()) as mocked_file:
				# GIVEN
				file_path = 'fake/file/path'
				content = 'My file content'
				mocked_file.side_effect = FileNotFoundError()

				# WHEN
				file_processor = FileProcessor(file_path)
				file_processor.append_line_into_file(content)

				# THEN
				# FileProcessorError exception was raised
