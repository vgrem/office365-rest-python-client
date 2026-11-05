from __future__ import annotations

from office365.directory.identitygovernance.entitlementmanagement.customextensioncalloutinstancestatus import (
    CustomExtensionCalloutInstanceStatus,
)
from office365.runtime.client_value import ClientValue


class CustomExtensionCalloutInstance(ClientValue):
    customExtensionId: str | None = None
    detail: str | None = None
    externalCorrelationId: str | None = None
    id: str | None = None
    status: CustomExtensionCalloutInstanceStatus = CustomExtensionCalloutInstanceStatus.calloutSent

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CustomExtensionCalloutInstance"
