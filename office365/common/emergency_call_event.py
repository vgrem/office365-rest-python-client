from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.communications.emergency_caller_info import EmergencyCallerInfo


class EmergencyCallEvent(Entity):
    @odata(name="callerInfo")
    @property
    def caller_info(self) -> EmergencyCallerInfo:
        """Gets the callerInfo property"""
        from office365.communications.emergency_caller_info import EmergencyCallerInfo

        return self.properties.get("callerInfo", EmergencyCallerInfo())

    @odata(name="emergencyNumberDialed")
    @property
    def emergency_number_dialed(self) -> Optional[str]:
        """Gets the emergencyNumberDialed property"""
        return self.properties.get("emergencyNumberDialed", None)

    @odata(name="policyName")
    @property
    def policy_name(self) -> Optional[str]:
        """Gets the policyName property"""
        return self.properties.get("policyName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EmergencyCallEvent"
