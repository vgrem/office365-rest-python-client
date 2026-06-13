from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.sitedesigns.image import SiteDesignImage
from office365.sharepoint.webs.teamappinfo import TeamAppInfo


@dataclass
class SiteDesignCreationInfo(ClientValue):
    """Args:
    Id (str or None): The ID of the site design to apply.
    Title (str or None): The display name of the site design.
    Description (str or None): The display description of site design.
    WebTemplate (str or None): Identifies which base template to add the design to. Use the value 64
    for the Team site template, and the value 68 for the Communication site template.
    SiteScriptIds (list[UUID] or None): A list of one or more site scripts. Each is identified by an ID.
    The scripts will run in the order listed.
    DesignPackageId (str or None):
    """

    Id = None
    Title: str | None = None
    Description: str | None = None
    WebTemplate: str | None = None
    SiteScriptIds: ClientValueCollection[uuid.UUID] | None = None
    SupportedWebTemplates: StringCollection | None = None
    ExpandedPreviewImages: ClientValueCollection[SiteDesignImage] = field(
        default_factory=lambda: ClientValueCollection(SiteDesignImage)
    )
    SupportedWebTemplateSubtypes: Optional[StringCollection] = None
    TargetPlatforms: Optional[StringCollection] = None
    TeamChannels: Optional[StringCollection] = None
    TeamImageAltText: Optional[str] = None
    TeamImageUrl: Optional[str] = None
    TeamInstalledApps: ClientValueCollection[TeamAppInfo] = field(
        default_factory=lambda: ClientValueCollection(TeamAppInfo)
    )
    TeamTemplate: Optional[str] = None
    TemplateAssets: Optional[StringCollection] = None
    TemplateFeatures: Optional[StringCollection] = None
    ThumbnailUrl: Optional[str] = None
    DesignPackageId: UUID | None = None
    DesignType: int | None = None
    InternalName: str | None = None
    IsCreationOnly: bool | None = None
    IsDefault: bool | None = None
    IsOutOfBoxTemplate: bool | None = None
    IsTenantAdminOnly: bool | None = None
    ListColor: int | None = None
    ListIcon: int | None = None
    PreviewImageAltText: str | None = None
    PreviewImageUrl: str | None = None
    RequiresClassConnected: bool | None = None
    RequiresGroupConnected: bool | None = None
    RequiresSyntexLicense: bool | None = None
    RequiresTeamsConnected: bool | None = None
    RequiresYammerConnected: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteDesignCreationInfo"
