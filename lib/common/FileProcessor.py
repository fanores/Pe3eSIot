"""File Processor"""
from lib.common.IotError import FileProcessorError


class FileProcessor:

    # constructor
    def __init__(self, file):
        self.file = file

    # append line into file
    def append_line_into_file(self, line):
        """
            Append Line Into a File
        """

        try:
            file = open(str(self.file), 'a+')
        except FileNotFoundError as error:
            raise FileProcessorError(print(error))

        file.write(line + "\n")
        file.close()
