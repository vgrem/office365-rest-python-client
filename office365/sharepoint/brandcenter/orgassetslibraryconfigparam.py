from typing import Optional

from office365.runtime.client_value import ClientValue


class OrgAssetsLibraryConfigParam(ClientValue):
    def __init__(
        self,
        is_copilot_searchable: Optional[bool] = None,
        is_copilot_searchable_present: Optional[bool] = None,
    ):
        self.IsCopilotSearchable = is_copilot_searchable
        self.IsCopilotSearchablePresent = is_copilot_searchable_present

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.BrandCenter.OrgAssetsLibraryConfigParam"
