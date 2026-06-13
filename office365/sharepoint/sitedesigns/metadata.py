from __future__ import annotations

from uuid import UUID

from office365.sharepoint.sitedesigns.creation_info import SiteDesignCreationInfo


class SiteDesignMetadata(SiteDesignCreationInfo):
    Id: UUID | None = None
    Order: int | None = None
    Version: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteDesignMetadata"
