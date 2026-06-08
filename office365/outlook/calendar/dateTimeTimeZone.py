from __future__ import annotations

from dataclasses import dataclass

import pytz

from office365.runtime.client_value import ClientValue


@dataclass
class DateTimeTimeZone(ClientValue):
    """Describes the date, time, and time zone of a point in time.

    Fields:
        dateTime (str | None): A single point of time in a combined date and time representation ({date}T{time};
            for example, 2017-08-29T04:00:00.0000000).
        timeZone (str | None): Represents a time zone, for example, "Pacific Standard Time".
    """

    dateTime: str | None = None
    timeZone: str | None = None

    def __repr__(self):
        return f"{self.dateTime or ''}, {self.timeZone or ''}"

    @staticmethod
    def parse(dt):
        """Parses from datetime

        Args:
            dt (datetime.datetime):
        """
        local_dt = dt.replace(tzinfo=pytz.utc)
        return DateTimeTimeZone(dateTime=local_dt.isoformat(), timeZone=local_dt.strftime("%Z"))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DateTimeTimeZone"
