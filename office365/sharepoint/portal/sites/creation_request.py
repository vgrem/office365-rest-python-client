from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection
from office365.sharepoint.teams.sp_team_channel_capabilities import SPTeamChannelCapabilities


@dataclass
class SPSiteCreationRequest(ClientValue):
    Title: str
    Url: str
    Owner: Optional[str] = None
    Lcid: int = 1033
    WebTemplate: str = "SITEPAGEPUBLISHING#0"
    AdditionalSiteFeatureIds: GuidCollection = field(default_factory=GuidCollection)
    AdditionalWebFeatureIds: GuidCollection = field(default_factory=GuidCollection)
    ChannelGroupId: Optional[str] = None
    Classification: Optional[str] = None
    Description: Optional[str] = None
    HubSiteId: Optional[str] = None
    RelatedGroupId: Optional[str] = None
    SensitivityLabel: Optional[str] = None
    SensitivityLabel2: Optional[str] = None
    ShareByEmailEnabled: Optional[bool] = None
    SiteDesignId: Optional[str] = None
    TeamsChannelType: Optional[int] = None
    TimeZoneId: Optional[int] = None
    WebTemplateExtensionId: Optional[str] = None
    ChannelCapabilities: SPTeamChannelCapabilities = field(default_factory=SPTeamChannelCapabilities)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.SPSiteCreationRequest"
