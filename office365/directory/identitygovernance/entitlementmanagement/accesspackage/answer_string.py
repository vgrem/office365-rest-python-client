from __future__ import annotations

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.answer import AccessPackageAnswer


class AccessPackageAnswerString(AccessPackageAnswer):
    value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageAnswerString"
