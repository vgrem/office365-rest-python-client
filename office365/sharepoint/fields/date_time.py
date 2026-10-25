from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.fields.field import Field


class FieldDateTime(Field):
    """Specifies a field that contains date and time values. To set properties, call the Update method
    (section 3.2.5.44.2.1.5)."""

    @odata(name="DateTimeCalendarType")
    @property
    def datetime_calendar_type(self) -> Optional[int]:
        """Gets the calendar type of the field"""
        return self.properties.get("DateTimeCalendarType", None)

    @datetime_calendar_type.setter
    def datetime_calendar_type(self, value: int) -> None:
        """Sets Gets the calendar type of the field"""
        self.set_property("DateTimeCalendarType", value)

    @odata(name="DateFormat")
    @property
    def date_format(self) -> Optional[str]:
        """ """
        return self.properties.get("DateFormat", None)

    @odata(name="DisplayFormat")
    @property
    def display_format(self) -> Optional[int]:
        """Specifies the type of date and time format that is used in the field"""
        return self.properties.get("DisplayFormat", None)

    @odata(name="FriendlyDisplayFormat")
    @property
    def friendly_display_format(self) -> Optional[int]:
        """Gets the type of friendly display format that is used in the field"""
        return self.properties.get("FriendlyDisplayFormat", None)

    @odata(name="TimeFormat")
    @property
    def time_format(self) -> Optional[str]:
        """Gets the time format that is used in the field"""
        return self.properties.get("TimeFormat", None)
