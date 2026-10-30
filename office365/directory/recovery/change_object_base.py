from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.recovery.recovery_action import RecoveryAction


class RecoveryChangeObjectBase(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="failureMessage")
    @property
    def failure_message(self) -> Optional[str]:
        """Gets the failureMessage property"""
        return self.properties.get("failureMessage", None)

    @odata(name="recoveryAction")
    @property
    def recovery_action(self) -> RecoveryAction:
        """Gets the recoveryAction property"""
        from office365.directory.recovery.recovery_action import RecoveryAction

        return self.properties.get("recoveryAction", RecoveryAction.softDelete)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.entraRecoveryServices.RecoveryChangeObjectBase"
