from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AccessReviewAccessPackageAssignmentPolicyScope(ClientValue):
    accessPackageDisplayName: str | None = None
    accessPackageId: str | None = None
    catalogDisplayName: str | None = None
    catalogId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewAccessPackageAssignmentPolicyScope"
