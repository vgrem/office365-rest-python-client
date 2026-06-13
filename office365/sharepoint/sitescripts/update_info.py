from __future__ import annotations

from uuid import UUID

from office365.sharepoint.sitescripts.creation_info import SiteScriptCreationInfo


class SiteScriptUpdateInfo(SiteScriptCreationInfo):
    Id: UUID | None = None
    Version: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteScriptUpdateInfo"
