from time import strftime, gmtime
import datetime


class Times():
    def get_monthDecimal():
        # Returns the current month as a decimal number i.e. 09
        return strftime("%m")

    @property
    def get_yearDecimal():
        # Returns the year with century as a decimal number
        return strftime("%Y")