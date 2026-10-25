from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class NotificationCallback(Entity):
    @odata(name="NotificationContext")
    @property
    def notification_context(self) -> Optional[str]:
        """Gets the NotificationContext property"""
        return self.properties.get("NotificationContext", None)

    @odata(name="NotificationEndpoint")
    @property
    def notification_endpoint(self) -> Optional[str]:
        """Gets the NotificationEndpoint property"""
        return self.properties.get("NotificationEndpoint", None)

    @odata(name="NotificationForwarderType")
    @property
    def notification_forwarder_type(self) -> Optional[str]:
        """Gets the NotificationForwarderType property"""
        return self.properties.get("NotificationForwarderType", None)

    @property
    def entity_type_name(self):
        return "SP.BusinessData.Runtime.NotificationCallback"
