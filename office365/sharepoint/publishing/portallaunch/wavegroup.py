from typing import Optional

from office365.runtime.client_value import ClientValue


class PortalLaunchWaveGroup(ClientValue):
    def __init__(self, id_: Optional[str] = None, site_url: Optional[str] = None, user_group_name: Optional[str] = None):
        self.Id = id_
        self.SiteUrl = site_url
        self.UserGroupName = user_group_name

    @property
    def entity_type_name(self):
        return "SP.Publishing.PortalLaunch.PortalLaunchWaveGroup"
