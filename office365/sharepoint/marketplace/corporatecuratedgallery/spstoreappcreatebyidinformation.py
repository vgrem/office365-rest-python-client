from office365.runtime.client_value import ClientValue


class SPStoreAppCreateByIdInformation(ClientValue):
    def __init__(
        self,
        caller_id: str = None,
        cmu: str = None,
        is_updating_app: bool = None,
        overwrite: bool = None,
        skip_feature_deployment: bool = None,
        store_asset_id: str = None,
    ):
        self.CallerId = caller_id
        self.CMU = cmu
        self.isUpdatingApp = is_updating_app
        self.Overwrite = overwrite
        self.SkipFeatureDeployment = skip_feature_deployment
        self.StoreAssetId = store_asset_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPStoreAppCreateByIdInformation"
