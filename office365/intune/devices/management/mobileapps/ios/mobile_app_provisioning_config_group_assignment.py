from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class MobileAppProvisioningConfigGroupAssignment(Entity):
    @odata(name="targetGroupId")
    @property
    def target_group_id(self) -> Optional[str]:
        """Gets the targetGroupId property"""
        return self.properties.get("targetGroupId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MobileAppProvisioningConfigGroupAssignment"
