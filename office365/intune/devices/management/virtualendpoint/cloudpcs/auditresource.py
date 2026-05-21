from __future__ import annotations

from dataclasses import dataclass, field

from office365.intune.devices.management.virtualendpoint.cloudpcs.auditproperty import CloudPcAuditProperty
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class CloudPcAuditResource(ClientValue):
    displayName: str | None = None
    modifiedProperties: ClientValueCollection[CloudPcAuditProperty] = field(
        default_factory=lambda: ClientValueCollection(CloudPcAuditProperty)
    )
    resourceId: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcAuditResource"
