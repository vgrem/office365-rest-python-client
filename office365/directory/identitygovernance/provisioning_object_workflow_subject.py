from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.identitygovernance.attribute_set_entry import AttributeSetEntry
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class ProvisioningObjectWorkflowSubject(ClientValue):
    attributeSetEntries: ClientValueCollection[AttributeSetEntry] = field(
        default_factory=lambda: ClientValueCollection(AttributeSetEntry)
    )
    id: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.ProvisioningObjectWorkflowSubject"
