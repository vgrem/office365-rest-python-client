from typing import Optional

from office365.runtime.client_value import ClientValue


class OrgLabelsContext(ClientValue):
    def __init__(
        self,
        display_name: Optional[str] = None,
        label_applicable_to: Optional[str] = None,
        object_id: Optional[str] = None,
    ):
        self.DisplayName = display_name
        self.LabelApplicableTo = label_applicable_to
        self.ObjectId = object_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.OrgLabelsContext"
