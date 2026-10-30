from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.key_value_pair import KeyValuePair
from office365.runtime.types.odata_property import odata


class ServiceAnnouncementBase(Entity):
    """This is an abstract base type for serviceHealthIssue and serviceUpdateMessage."""

    @odata(name="details")
    @property
    def details(self) -> ClientValueCollection[KeyValuePair]:
        """Gets the details property"""
        return self.properties.get("details", ClientValueCollection[KeyValuePair](KeyValuePair))

    @odata(name="endDateTime")
    @property
    def end_date_time(self) -> Optional[datetime]:
        """Gets the endDateTime property"""
        return self.properties.get("endDateTime", datetime.min)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="startDateTime")
    @property
    def start_date_time(self) -> Optional[datetime]:
        """Gets the startDateTime property"""
        return self.properties.get("startDateTime", datetime.min)

    @odata(name="title")
    @property
    def title(self) -> Optional[str]:
        """Gets the title property"""
        return self.properties.get("title", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ServiceAnnouncementBase"
