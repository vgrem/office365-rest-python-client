from __future__ import annotations

from office365.runtime.client_value import ClientValue


class DateTimeColumn(ClientValue):
    """The dateTimeColumn on a columnDefinition resource indicates that the column's values are dates or times."""

    def __init__(self, display_as: str | None = None, display_format: str | None = None):
        """
        :param str display_as: How the value should be presented in the UX. Must be one of default, friendly,
             or standard. See below for more details. If unspecified, treated as default.
        :param str display_format: Indicates whether the value should be presented as a date only or a date and time.
            Must be one of dateOnly or dateTime
        """
        self.displayAs = display_as
        self.format = display_format
