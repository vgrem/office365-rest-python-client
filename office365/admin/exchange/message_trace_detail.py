from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class ExchangeMessageTraceDetail(Entity):
    @odata(name="action")
    @property
    def action(self) -> Optional[str]:
        """Gets the action property"""
        return self.properties.get("action", None)

    @odata(name="data")
    @property
    def data(self) -> Optional[str]:
        """Gets the data property"""
        return self.properties.get("data", None)

    @odata(name="dateTime")
    @property
    def date_time(self) -> datetime:
        """Gets the dateTime property"""
        return self.properties.get("dateTime", datetime.min)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="event")
    @property
    def event(self) -> Optional[str]:
        """Gets the event property"""
        return self.properties.get("event", None)

    @odata(name="messageId")
    @property
    def message_id(self) -> Optional[str]:
        """Gets the messageId property"""
        return self.properties.get("messageId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ExchangeMessageTraceDetail"
