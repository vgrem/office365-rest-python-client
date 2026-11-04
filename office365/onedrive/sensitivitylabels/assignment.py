from __future__ import annotations

from office365.onedrive.sensitivitylabels.assignment_method import SensitivityLabelAssignmentMethod
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SensitivityLabelAssignment(ClientValue):
    """Provides details about a sensitivity label assigned to a file in SharePoint or OneDrive for Business."""

    assignmentMethod: SensitivityLabelAssignmentMethod | None = None
    sensitivityLabelId: str | None = None
    tenantId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SensitivityLabelAssignment"
