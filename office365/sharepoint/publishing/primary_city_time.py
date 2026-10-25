from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class PrimaryCityTime(Entity):
    """Represents the date and time, in UTC, of the geographic location."""

    @odata(name="Location")
    @property
    def location(self) -> Optional[str]:
        """ """
        return self.properties.get("Location", None)

    @odata(name="Time")
    @property
    def time(self) -> Optional[str]:
        """"""
        return self.properties.get("Time", None)

    @odata(name="UtcOffset")
    @property
    def utc_offset(self) -> Optional[str]:
        """"""
        return self.properties.get("UtcOffset", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.PrimaryCityTime"
