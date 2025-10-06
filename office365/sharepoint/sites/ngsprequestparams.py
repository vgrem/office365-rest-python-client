from office365.runtime.client_value import ClientValue
from office365.sharepoint.sites.followedsitesparams import FollowedSitesParams


class NgspRequestParams(ClientValue):

    def __init__(self, followed_sites: FollowedSitesParams = FollowedSitesParams()):
        self.FollowedSites = followed_sites
