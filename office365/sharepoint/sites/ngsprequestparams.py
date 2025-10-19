from office365.runtime.client_value import ClientValue
from office365.sharepoint.sites.followedsitesparams import FollowedSitesParams
from office365.sharepoint.sites.ownedbymeparams import OwnedByMeParams
from office365.sharepoint.sites.recentfilesparams import RecentFilesParams


class NgspRequestParams(ClientValue):

    def __init__(
        self,
        followed_sites: FollowedSitesParams = FollowedSitesParams(),
        recent_files: RecentFilesParams = RecentFilesParams(),
        owned_by_me: OwnedByMeParams = OwnedByMeParams(),
    ):
        self.FollowedSites = followed_sites
        self.RecentFiles = recent_files
        self.OwnedByMe = owned_by_me
