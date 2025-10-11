from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.portallaunch.wavegroup import PortalLaunchWaveGroup


class PortalLaunchWave(ClientValue):

    def __init__(
        self,
        groups: ClientValueCollection[PortalLaunchWaveGroup] = ClientValueCollection(PortalLaunchWaveGroup),
        launch_date_utc: datetime = None,
        name: str = None,
        order: int = None,
    ):
        self.Groups = groups
        self.LaunchDateUtc = launch_date_utc
        self.Name = name
        self.Order = order

    @property
    def entity_type_name(self):
        return "SP.Publishing.PortalLaunch.PortalLaunchWave"
