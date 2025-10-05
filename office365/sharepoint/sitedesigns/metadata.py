from office365.sharepoint.sitedesigns.creation_info import SiteDesignCreationInfo


class SiteDesignMetadata(SiteDesignCreationInfo):

    def __init__(self, order=None, version=None, id_: str = None):
        super().__init__()
        self.Order = order
        self.Version = version
        self.Id = id_

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteDesignMetadata"
