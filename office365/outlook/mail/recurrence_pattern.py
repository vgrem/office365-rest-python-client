from office365.outlook.calendar.dayofweek import DayOfWeek
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class RecurrencePattern(ClientValue):
    """Describes the frequency by which a recurring event repeats."""

    def __init__(
        self,
        day_of_month=None,
        days_of_week: DayOfWeek = None,
        first_day_of_week=None,
        index: int = None,
        interval: int = None,
        month: int = None,
        pattern_type: str = None,
    ):
        """
        :param int day_of_month: The day of the month on which the event occurs. Required if type is absoluteMonthly
            or absoluteYearly.
        :param list[DayOfWeek] days_of_week: A collection of the days of the week on which the event occurs
        :param DayOfWeek first_day_of_week: The first day of the week
        :param str index: Specifies on which instance of the allowed days specified in daysOfWeek the event occurs,
             counted from the first instance in the month.
        :param int interval: The number of units between occurrences, where units can be in days, weeks, months,
             or years, depending on the type. Required.
        :param int month: The month in which the event occurs. This is a number from 1 to 12.
        :param str pattern_type: The recurrence pattern type: daily, weekly, absoluteMonthly, relativeMonthly,
             absoluteYearly, relativeYearly
        """
        self.dayOfMonth = day_of_month
        self.daysOfWeek = ClientValueCollection(DayOfWeek, days_of_week)
        self.firstDayOfWeek = first_day_of_week
        self.index = index
        self.interval = interval
        self.month = month
        self.type = pattern_type
