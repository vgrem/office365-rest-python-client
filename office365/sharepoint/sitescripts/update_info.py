from office365.sharepoint.sitescripts.creation_info import SiteScriptCreationInfo


class SiteScriptUpdateInfo(SiteScriptCreationInfo):

    def __init__(self, id_: str = None, version: int = None):
        super().__init__()
        self.Id = id_
        self.Version = version

    @property
    def entity_type_name(self):
        return (
            "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteScriptUpdateInfo"
        )
