from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AccessPackageAssignmentRequestParameters(ClientValue):
    bypassApproval: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageAssignmentRequestParameters"
