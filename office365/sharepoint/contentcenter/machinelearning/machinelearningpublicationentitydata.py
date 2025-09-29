from office365.runtime.client_value import ClientValue


class SPMachineLearningPublicationEntityData(ClientValue):

    def __init__(
        self,
        model_unique_id: str = None,
        remove_site_promotion_enabled: bool = None,
        target_library_server_relative_url: str = None,
        target_site_url: str = None,
        target_table_list_server_relative_url: str = None,
        target_web_server_relative_url: str = None,
        view_option: str = None,
    ):
        self.ModelUniqueId = model_unique_id
        self.RemoveSitePromotionEnabled = remove_site_promotion_enabled
        self.TargetLibraryServerRelativeUrl = target_library_server_relative_url
        self.TargetSiteUrl = target_site_url
        self.TargetTableListServerRelativeUrl = target_table_list_server_relative_url
        self.TargetWebServerRelativeUrl = target_web_server_relative_url
        self.ViewOption = view_option
