from office365.onedrive.sensitivitylabels.assignment_method import (
    SensitivityLabelAssignmentMethod,
)
from office365.runtime.client_value import ClientValue


class SensitivityLabelAssignment(ClientValue):
    """Provides details about a sensitivity label assigned to a file in SharePoint or OneDrive for Business."""

    def __init__(
        self,
        assignment_method: SensitivityLabelAssignmentMethod = None,
        sensitivity_label_id: str = None,
        tenant_id: str = None,
    ):
        """
        :param str assignment_method: Indicates whether the label assignment is done automatically, as a standard,
            or a privileged operation.
        :param str sensitivity_label_id: The unique identifier for the sensitivity label assigned to the file.
        : 	The unique identifier for the tenant that hosts the file when this label is applied.
        :param str tenant_id: The unique identifier for the tenant that hosts the file when this label is applied.
        """
        self.assignmentMethod = assignment_method
        self.sensitivityLabelId = sensitivity_label_id
        self.tenantId = tenant_id
