from __future__ import annotations

from dataclasses import field

from office365.security.datasecurity.integrated_application_metadata import IntegratedApplicationMetadata
from office365.security.datasecurity.policy_location import PolicyLocation


class ProtectedApplicationMetadata(IntegratedApplicationMetadata):
    applicationLocation: PolicyLocation = field(default_factory=PolicyLocation)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ProtectedApplicationMetadata"
