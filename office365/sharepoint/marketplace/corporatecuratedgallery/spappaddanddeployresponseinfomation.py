from office365.runtime.client_value import ClientValue


class SPAppAddAndDeployResponseInfomation(ClientValue):

    def __init__(
        self,
        is_first_time_deployed: bool = None,
        list_id: str = None,
        list_item_id: str = None,
        list_item_unique_id: str = None,
    ):
        self.IsFirstTimeDeployed = is_first_time_deployed
        self.ListId = list_id
        self.ListItemId = list_item_id
        self.ListItemUniqueId = list_item_unique_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPAppAddAndDeployResponseInfomation"
