from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.resource_attribute_destination import (
    AccessPackageResourceAttributeDestination,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.resource_attribute_source import (
    AccessPackageResourceAttributeSource,
)
from office365.runtime.client_value import ClientValue


@dataclass
class AccessPackageResourceAttribute(ClientValue):
    destination: AccessPackageResourceAttributeDestination = field(
        default_factory=AccessPackageResourceAttributeDestination
    )
    isEditable: bool | None = None
    isPersistedOnAssignmentRemoval: bool | None = None
    name: str | None = None
    source: AccessPackageResourceAttributeSource = field(default_factory=AccessPackageResourceAttributeSource)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageResourceAttribute"
