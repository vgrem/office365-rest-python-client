from typing import Optional

from office365.sharepoint.sitescripts.creation_info import SiteScriptCreationInfo


class SiteScriptUpdateInfo(SiteScriptCreationInfo):
    def __init__(self, id_: Optional[str] = None, version: Optional[int] = None):
        super().__init__()
        self.Id = id_
        self.Version = version

    @property
    def entity_type_name(self) -> str:  # type: ignore[override]
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteScriptUpdateInfo"
