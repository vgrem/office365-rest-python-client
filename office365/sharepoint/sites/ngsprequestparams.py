from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sitedesigns.favorited_items_params import FavoritedItemsParams
from office365.sharepoint.sites.followedsitesparams import FollowedSitesParams
from office365.sharepoint.sites.ownedbymeparams import OwnedByMeParams
from office365.sharepoint.sites.recent_sites_params import RecentSitesParams
from office365.sharepoint.sites.recentfilesparams import RecentFilesParams
from office365.sharepoint.sites.suggested_sites_params import SuggestedSitesParams


@dataclass
class NgspRequestParams(ClientValue):
    FollowedSites: FollowedSitesParams = field(default_factory=FollowedSitesParams)
    RecentFiles: RecentFilesParams = field(default_factory=RecentFilesParams)
    OwnedByMe: OwnedByMeParams = field(default_factory=OwnedByMeParams)
    FavoritedItems: FavoritedItemsParams = field(default_factory=FavoritedItemsParams)
    RecentSites: RecentSitesParams = field(default_factory=RecentSitesParams)
    SuggestedSites: SuggestedSitesParams = field(default_factory=SuggestedSitesParams)
