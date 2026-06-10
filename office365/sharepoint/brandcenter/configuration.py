from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.sharepoint.administration.orgassets.org_assets import OrgAssets
from office365.sharepoint.types.resource_path import ResourcePath
from office365.sharepoint.types.resource_path import ResourcePath as SPResPath


@dataclass
class BrandCenterConfiguration(ClientValue):
    BrandColorsListId: Optional[str] = None
    BrandColorsListUrl: Optional[str] = None
    BrandFontLibraryId: Optional[str] = None
    BrandFontLibraryUrl: SPResPath = field(default_factory=SPResPath)
    IsBrandCenterSiteFeatureEnabled: Optional[bool] = None
    IsPublicCdnEnabled: Optional[bool] = None
    OrgAssets: OrgAssets = field(default_factory=OrgAssets)
    SiteId: Optional[str] = None
    SiteUrl: Optional[str] = None
    OrgSkillsLibraryId: UUID | None = None
    OrgSkillsLibraryUrl: ResourcePath = field(default_factory=ResourcePath)
