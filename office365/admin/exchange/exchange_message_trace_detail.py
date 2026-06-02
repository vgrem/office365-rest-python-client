from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity


class ExchangeMessageTraceDetail(Entity):
    @property
    def action(self) -> Optional[str]:
        """Gets the action property"""
        return self.properties.get("action", None)

    @property
    def data(self) -> Optional[str]:
        """Gets the data property"""
        return self.properties.get("data", None)

    @property
    def date_time(self) -> datetime:
        """Gets the dateTime property"""
        return self.properties.get("dateTime", datetime.min)

    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @property
    def event(self) -> Optional[str]:
        """Gets the event property"""
        return self.properties.get("event", None)

    @property
    def message_id(self) -> Optional[str]:
        """Gets the messageId property"""
        return self.properties.get("messageId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ExchangeMessageTraceDetail"
