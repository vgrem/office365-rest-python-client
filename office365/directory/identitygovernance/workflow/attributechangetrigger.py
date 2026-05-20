from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.identitygovernance.workflow.triggerattribute import TriggerAttribute
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class AttributeChangeTrigger(ClientValue):
    triggerAttributes: ClientValueCollection[TriggerAttribute] = field(
        default_factory=lambda: ClientValueCollection(TriggerAttribute)
    )

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.AttributeChangeTrigger"
