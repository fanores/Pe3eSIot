""" Date and Time"""
from datetime import datetime


class DateTime:

    # returns date in a string format
    def get_current_date(self, delimiter="."):
        """
            Get Current Date: returns the date in a string format
        :return: date as string
        """
        now = datetime.now()

        return now.strftime("%m" + delimiter + "%d" + delimiter + "%Y")

    # returns time in a string format
    def get_current_time(self, include_seconds: True):
        """
            Get Current Time: returns the time in a string format
        :return: time as string
        """
        now = datetime.now()

        if include_seconds:
            return now.strftime("%H:%M:%S")
        else:
            return now.strftime("%H:%M")

    # returns full weekday name
    def get_current_weekday_name_full(self):
        """
            Get Current Weekday Full Name: returns the full weekday name
        @return: full weekday name as string
        """
        now = datetime.now()

        return now.strftime("%A")

    # returns abbreviated weekday name
    def get_current_weekday_name_abbreviated(self):
        """
            Get Current Weekday Name Abbreviated: returns the abbreviated weekday name
        @return: abbreviated weekday name as string
        """
        now = datetime.now()

        return now.strftime("%a")

    # returns full month name
    def get_current_month_name_full(self):
        """
            Get Current Month Full Name: returns the full month name
        @return: full month name as string
        """
        now = datetime.now()

        return now.strftime("%B")

    # returns abbreviated month name
    def get_current_month_name_abbreviated(self):
        """
            Get Current Month Name Abbreviated: returns the abbreviated month name
        @return: abbreviated month name as string
        """
        now = datetime.now()

        return now.strftime("%b")
