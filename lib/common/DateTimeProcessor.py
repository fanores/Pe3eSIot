""" Date and Time Processor"""
from datetime import datetime


class DateTimeProcessor:

    # constructor
    def __init__(self, now):

        self.now = now

    # returns date for a datetime object as a string
    def get_date(self, delimiter="."):
        """
            Get Date: returns the date in a string format
        :return: date as string
        """

        return self.now.strftime("%-d" + delimiter + "%-m" + delimiter + "%Y")

    # set date and time for DateTimeProcessor
    def set_date_time(self, now):
        self.now = now

    # returns time for a datetime object as a string
    def get_time(self, include_seconds=True):
        """
            Get Time: returns the time in a string format
        :return: time as string
        """

        if include_seconds:
            return self.now.strftime("%-H:%-M:%-S")
        else:
            return self.now.strftime("%-H:%-M")

    # returns full weekday name
    def get_full_weekday_name(self):
        """
            Get Weekday Full Name: returns the full weekday name
        @return: full weekday name as string
        """

        return self.now.strftime("%A")

    # returns abbreviated weekday name
    def get_abbreviated_weekday_name(self):
        """
            Get Weekday Name Abbreviated: returns the abbreviated weekday name
        @return: abbreviated weekday name as string
        """

        return self.now.strftime("%a")

    # returns full month name
    def get_full_month_name(self):
        """
            Get Month Full Name: returns the full month name
        @return: full month name as string
        """

        return self.now.strftime("%B")

    # returns abbreviated month name
    def get_abbreviated_month_name(self):
        """
            Get Month Name Abbreviated: returns the abbreviated month name
        @return: abbreviated month name as string
        """

        return self.now.strftime("%b")
