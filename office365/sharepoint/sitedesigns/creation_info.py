from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.sitedesigns.image import SiteDesignImage
from office365.sharepoint.webs.teamappinfo import TeamAppInfo


@dataclass
class SiteDesignCreationInfo(ClientValue):
    """Args:
        _id (str or None): The ID of the site design to apply.
        title (str or None): The display name of the site design.
        description (str or None): The display description of site design.
        web_template (str or None): Identifies which base template to add the design to. Use the value 64 for the Team site template, and the value 68 for the Communication site template.
        site_script_ids (list[UUID] or None): A list of one or more site scripts. Each is identified by an ID. The scripts will run in the order listed.
        design_package_id (str or None):
    """

    Id = None
    Title: str | None = None
    Description: str | None = None
    WebTemplate: str | None = None
    SiteScriptIds: ClientValueCollection[uuid.UUID] | None = None
    DesignPackageId = None
    DesignType = None
    InternalName = None
    IsDefault = None
    IsOutOfBoxTemplate = None
    IsTenantAdminOnly = None
    ListColor = None
    ListIcon = None
    PreviewImageAltText = None
    PreviewImageUrl = None
    RequiresClassConnected = None
    RequiresGroupConnected = None
    RequiresSyntexLicense = None
    RequiresTeamsConnected = None
    RequiresYammerConnected = None
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

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteDesignCreationInfo"
