from office365.runtime.client_value import ClientValue
from office365.sharepoint.recentfilesparams import RecentFilesParams
from office365.sharepoint.sites.followedsitesparams import FollowedSitesParams


class NgspRequestParams(ClientValue):

    def __init__(
        self,
        followed_sites: FollowedSitesParams = FollowedSitesParams(),
        recent_files: RecentFilesParams = RecentFilesParams(),
    ):
        self.FollowedSites = followed_sites
        self.RecentFiles = recent_files
