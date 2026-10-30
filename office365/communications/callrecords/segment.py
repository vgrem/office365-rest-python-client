from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.communications.callrecords.endpoint import Endpoint
from office365.communications.callrecords.failure_info import FailureInfo
from office365.communications.callrecords.media import Media
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata


class Segment(Entity):
    """Represents a portion of a User-User communication or a User-Meeting communication in the case of a
    Conference call. A typical VOIP call will have one segment per session. In certain scenarios, such as PSTN calls,
    there will be multiple segments per session due to additional server-to-server communication required to connect
    the call."""

    @odata(name="callee")
    @property
    def callee(self) -> Endpoint:
        """Endpoint that answered this segment."""
        return self.properties.get("callee", Endpoint())

    @odata(name="caller")
    @property
    def caller(self) -> Endpoint:
        """Endpoint that initiated this segment."""
        return self.properties.get("caller", Endpoint())

    @property
    def entity_type_name(self):
        return "microsoft.graph.callRecords.segment"

    @odata(name="endDateTime")
    @property
    def end_date_time(self) -> Optional[datetime]:
        """Gets the endDateTime property"""
        return self.properties.get("endDateTime", datetime.min)

    @odata(name="failureInfo")
    @property
    def failure_info(self) -> FailureInfo:
        """Gets the failureInfo property"""
        return self.properties.get("failureInfo", FailureInfo())

    @odata(name="media")
    @property
    def media(self) -> ClientValueCollection[Media]:
        """Gets the media property"""
        return self.properties.get("media", ClientValueCollection[Media](Media))

    @odata(name="startDateTime")
    @property
    def start_date_time(self) -> Optional[datetime]:
        """Gets the startDateTime property"""
        return self.properties.get("startDateTime", datetime.min)
