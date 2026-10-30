from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class AzureCommunicationServicesUserConversationMember(Entity):
    @odata(name="azureCommunicationServicesId")
    @property
    def azure_communication_services_id(self) -> Optional[str]:
        """Gets the azureCommunicationServicesId property"""
        return self.properties.get("azureCommunicationServicesId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AzureCommunicationServicesUserConversationMember"
