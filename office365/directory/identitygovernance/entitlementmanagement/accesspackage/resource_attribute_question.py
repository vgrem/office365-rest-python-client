from __future__ import annotations

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.question import AccessPackageQuestion
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AccessPackageResourceAttributeQuestion(ClientValue):
    question: AccessPackageQuestion | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageResourceAttributeQuestion"
