"""FVE File Writer"""
from lib.common.FileProcessor import FileProcessor
from lib.common.IotError import FileProcessorError
from lib.common.IotError import FveFileReporterError


class FveFileReporter:
    # constants
    ELEMENT_NOT_AVAILABLE = "N/A"
    SEMICOLON = ";"

    # constructor
    def __init__(self, file):
        self.file_processor = FileProcessor(file)

    # write any FVE measurements to file
    def write_measurements_to_file(self, measurements, kpis):
        """
            Write FVE measurements to a SEMICOLON separated file.
            Interested only in the requested FVE kpis.
        """
        line = ''
        for kpi in kpis:
            kpi_value = measurements.get(kpi, self.ELEMENT_NOT_AVAILABLE)

            # store kpi if it is available
            if kpi_value != self.ELEMENT_NOT_AVAILABLE:
                line = line + kpi_value + self.SEMICOLON

        try:
            if line != '':
                self.file_processor.append_line_into_file(line)
        except FileProcessorError as error:
            raise FveFileReporterError(error.message)
