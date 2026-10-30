from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.virtualendpoint.cloudpcs.auditactivityoperationtype import (
        CloudPcAuditActivityOperationType,
    )
    from office365.intune.devices.management.virtualendpoint.cloudpcs.auditactivityresult import (
        CloudPcAuditActivityResult,
    )
    from office365.intune.devices.management.virtualendpoint.cloudpcs.auditactor import (
        CloudPcAuditActor,
    )
    from office365.intune.devices.management.virtualendpoint.cloudpcs.auditcategory import (
        CloudPcAuditCategory,
    )
    from office365.intune.devices.management.virtualendpoint.cloudpcs.auditresource import (
        CloudPcAuditResource,
    )


class CloudPcAuditEvent(Entity):
    @odata(name="activity")
    @property
    def activity(self) -> Optional[str]:
        """Gets the activity property"""
        return self.properties.get("activity", None)

    @odata(name="activityDateTime")
    @property
    def activity_date_time(self) -> Optional[datetime]:
        """Gets the activityDateTime property"""
        return self.properties.get("activityDateTime", datetime.min)

    @odata(name="activityOperationType")
    @property
    def activity_operation_type(self) -> CloudPcAuditActivityOperationType:
        """Gets the activityOperationType property"""
        from office365.intune.devices.management.virtualendpoint.cloudpcs.auditactivityoperationtype import (
            CloudPcAuditActivityOperationType,
        )

        return self.properties.get("activityOperationType", CloudPcAuditActivityOperationType.create)

    @odata(name="activityResult")
    @property
    def activity_result(self) -> CloudPcAuditActivityResult:
        """Gets the activityResult property"""
        from office365.intune.devices.management.virtualendpoint.cloudpcs.auditactivityresult import (
            CloudPcAuditActivityResult,
        )

        return self.properties.get("activityResult", CloudPcAuditActivityResult.success)

    @odata(name="activityType")
    @property
    def activity_type(self) -> Optional[str]:
        """Gets the activityType property"""
        return self.properties.get("activityType", None)

    @odata(name="actor")
    @property
    def actor(self) -> CloudPcAuditActor:
        """Gets the actor property"""
        from office365.intune.devices.management.virtualendpoint.cloudpcs.auditactor import (
            CloudPcAuditActor,
        )

        return self.properties.get("actor", CloudPcAuditActor())

    @odata(name="category")
    @property
    def category(self) -> CloudPcAuditCategory:
        """Gets the category property"""
        from office365.intune.devices.management.virtualendpoint.cloudpcs.auditcategory import (
            CloudPcAuditCategory,
        )

        return self.properties.get("category", CloudPcAuditCategory.cloudPC)

    @odata(name="componentName")
    @property
    def component_name(self) -> Optional[str]:
        """Gets the componentName property"""
        return self.properties.get("componentName", None)

    @odata(name="correlationId")
    @property
    def correlation_id(self) -> Optional[str]:
        """Gets the correlationId property"""
        return self.properties.get("correlationId", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="resources")
    @property
    def resources(self) -> ClientValueCollection[CloudPcAuditResource]:
        """Gets the resources property"""
        from office365.intune.devices.management.virtualendpoint.cloudpcs.auditresource import (
            CloudPcAuditResource,
        )

        return self.properties.get("resources", ClientValueCollection[CloudPcAuditResource](CloudPcAuditResource))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudPcAuditEvent"
