from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.common.error_code import ErrorCode
from office365.common.policy_set_status import PolicySetStatus
from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version


@version("beta")
class PolicySetItem(Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="errorCode")
    @property
    def error_code(self) -> Optional[ErrorCode]:
        """Gets the errorCode property"""
        return self.properties.get("errorCode", None)

    @odata(name="guidedDeploymentTags")
    @property
    def guided_deployment_tags(self) -> StringCollection:
        """Gets the guidedDeploymentTags property"""
        return self.properties.get("guidedDeploymentTags", StringCollection())

    @odata(name="itemType")
    @property
    def item_type(self) -> Optional[str]:
        """Gets the itemType property"""
        return self.properties.get("itemType", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="payloadId")
    @property
    def payload_id(self) -> Optional[str]:
        """Gets the payloadId property"""
        return self.properties.get("payloadId", None)

    @odata(name="status")
    @property
    def status(self) -> Optional[PolicySetStatus]:
        """Gets the status property"""
        return self.properties.get("status", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PolicySetItem"
