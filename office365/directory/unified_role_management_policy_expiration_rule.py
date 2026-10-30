from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.runtime.types.duration import timedelta


class UnifiedRoleManagementPolicyExpirationRule(Entity):
    @odata(name="isExpirationRequired")
    @property
    def is_expiration_required(self) -> Optional[bool]:
        """Gets the isExpirationRequired property"""
        return self.properties.get("isExpirationRequired", None)

    @odata(name="maximumDuration")
    @property
    def maximum_duration(self) -> Optional[timedelta]:
        """Gets the maximumDuration property"""
        return self.properties.get("maximumDuration", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UnifiedRoleManagementPolicyExpirationRule"
