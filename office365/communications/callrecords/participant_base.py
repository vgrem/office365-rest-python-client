from __future__ import annotations

from office365.communications.callrecords.administrative_unit_info import AdministrativeUnitInfo
from office365.communications.virtualevents.communications_identity_set import CommunicationsIdentitySet
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata


class ParticipantBase(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.callRecords.ParticipantBase"

    @odata(name="administrativeUnitInfos")
    @property
    def administrative_unit_infos(self) -> ClientValueCollection[AdministrativeUnitInfo]:
        """Gets the administrativeUnitInfos property"""
        return self.properties.get(
            "administrativeUnitInfos", ClientValueCollection[AdministrativeUnitInfo](AdministrativeUnitInfo)
        )

    @odata(name="identity")
    @property
    def identity(self) -> CommunicationsIdentitySet:
        """Gets the identity property"""
        return self.properties.get("identity", CommunicationsIdentitySet())
