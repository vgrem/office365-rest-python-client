from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class PortalLaunchWaveGroup(ClientValue):
    Id: Optional[str] = None
    SiteUrl: Optional[str] = None
    UserGroupName: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.PortalLaunch.PortalLaunchWaveGroup"
