from typing import Optional

from office365.runtime.client_value import ClientValue


class OrgAssetsLibraryConfigParam(ClientValue):
    IsCopilotSearchable: Optional[bool] = None
    IsCopilotSearchablePresent: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.BrandCenter.OrgAssetsLibraryConfigParam"
