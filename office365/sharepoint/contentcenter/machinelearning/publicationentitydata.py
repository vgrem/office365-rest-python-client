from typing import Optional

from office365.runtime.client_value import ClientValue


class SPMachineLearningPublicationEntityData(ClientValue):
    def __init__(
        self,
        model_unique_id: Optional[str] = None,
        remove_site_promotion_enabled: Optional[bool] = None,
        target_library_server_relative_url: Optional[str] = None,
        target_site_url: Optional[str] = None,
        target_table_list_server_relative_url: Optional[str] = None,
        target_web_server_relative_url: Optional[str] = None,
        view_option: Optional[str] = None,
    ):
        self.ModelUniqueId = model_unique_id
        self.RemoveSitePromotionEnabled = remove_site_promotion_enabled
        self.TargetLibraryServerRelativeUrl = target_library_server_relative_url
        self.TargetSiteUrl = target_site_url
        self.TargetTableListServerRelativeUrl = target_table_list_server_relative_url
        self.TargetWebServerRelativeUrl = target_web_server_relative_url
        self.ViewOption = view_option

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPMachineLearningPublicationEntityData"
