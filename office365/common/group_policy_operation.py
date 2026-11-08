from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.common.group_policy_operation_status import GroupPolicyOperationStatus
from office365.common.group_policy_operation_type import GroupPolicyOperationType
from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class GroupPolicyOperation(Entity):
    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="operationStatus")
    @property
    def operation_status(self) -> Optional[GroupPolicyOperationStatus]:
        """Gets the operationStatus property"""
        return self.properties.get("operationStatus", None)

    @odata(name="operationType")
    @property
    def operation_type(self) -> Optional[GroupPolicyOperationType]:
        """Gets the operationType property"""
        return self.properties.get("operationType", None)

    @odata(name="statusDetails")
    @property
    def status_details(self) -> Optional[str]:
        """Gets the statusDetails property"""
        return self.properties.get("statusDetails", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicyOperation"
