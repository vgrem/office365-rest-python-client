from office365.runtime.client_value import ClientValue


class AssignedLabel(ClientValue):
    """
    Represents a sensitivity label assigned to a Microsoft 365 group. Sensitivity labels allow administrators
    to enforce specific group settings on a group by assigning a classification to the group (such as Confidential,
    Highly Confidential or General). Sensitivity labels are published by administrators in Microsoft 365 Security and
    Compliance Center as part of Microsoft Purview Information Protection capabilities. For more information about
    sensitivity labels, see Sensitivity labels overview.
    """

    def __init__(self, display_name: str = None, label_id: str = None):
        self.displayName = display_name
        self.labelId = label_id
