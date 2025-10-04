from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.publishing.webpartdetailswrapper import WebPartDetailsWrapper


class SitePageDependencyMetadata(ClientValue):
    """ """

    def __init__(
        self,
        dependency_item_path=None,
        is_in_page_site_assets_folder=None,
        list_id=None,
        related_web_parts=None,
        site_id=None,
        related_web_parts_details: ClientValueCollection[
            WebPartDetailsWrapper
        ] = ClientValueCollection(WebPartDetailsWrapper),
        type_: str = None,
        unique_id: str = None,
        web_id: str = None,
    ):
        self.DependencyItemPath = dependency_item_path
        self.IsInPageSiteAssetsFolder = is_in_page_site_assets_folder
        self.ListId = list_id
        self.RelatedWebParts = StringCollection(related_web_parts)
        self.SiteId = site_id
        self.RelatedWebPartsDetails = related_web_parts_details
        self.Type = type_
        self.UniqueId = unique_id
        self.WebId = web_id

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageDependencyMetadata"
