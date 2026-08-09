from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.applications.custom_security_attribute_exemption import CustomSecurityAttributeExemption
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class AppManagementPolicyActorExemptions(ClientValue):
    customSecurityAttributes: ClientValueCollection[CustomSecurityAttributeExemption] = field(
        default_factory=lambda: ClientValueCollection(CustomSecurityAttributeExemption)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AppManagementPolicyActorExemptions"
