from __future__ import annotations

import uuid
from typing import Optional


from dataclasses import dataclass, field
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.sitedesigns.image import SiteDesignImage
from office365.sharepoint.webs.teamappinfo import TeamAppInfo


@dataclass
class SiteDesignCreationInfo(ClientValue):

    """
    :param str or None _id: The ID of the site design to apply.
    :param str or None title: The display name of the site design.
    :param str or None description: The display description of site design.
    :param str or None web_template: Identifies which base template to add the design to. Use the value 64 for the
    Team site template, and the value 68 for the Communication site template.
    :param list[UUID] or None site_script_ids: A list of one or more site scripts. Each is identified by an ID.
    The scripts will run in the order listed.
    :param str or None design_package_id:
    """

    Id = None
    Title = None
    Description = None
    WebTemplate = None
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