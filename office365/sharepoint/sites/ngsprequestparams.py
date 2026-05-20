from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sites.followedsitesparams import FollowedSitesParams
from office365.sharepoint.sites.ownedbymeparams import OwnedByMeParams
from office365.sharepoint.sites.recentfilesparams import RecentFilesParams


@dataclass
class NgspRequestParams(ClientValue):
    FollowedSites: FollowedSitesParams = field(default_factory=FollowedSitesParams)
    RecentFiles: RecentFilesParams = field(default_factory=RecentFilesParams)
    OwnedByMe: OwnedByMeParams = field(default_factory=OwnedByMeParams)
