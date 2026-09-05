from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.localized_text import (
    AccessPackageLocalizedText,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class AccessPackageAnswerChoice(ClientValue):
    actualValue: str | None = None
    text: str | None = None
    localizations: ClientValueCollection[AccessPackageLocalizedText] = field(
        default_factory=lambda: ClientValueCollection(AccessPackageLocalizedText)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageAnswerChoice"
