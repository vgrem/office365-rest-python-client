from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.portallaunch.wavegroup import PortalLaunchWaveGroup


@dataclass
class PortalLaunchWave(ClientValue):
    Groups: ClientValueCollection[PortalLaunchWaveGroup] = field(
        default_factory=lambda: ClientValueCollection(PortalLaunchWaveGroup)
    )
    LaunchDateUtc: Optional[datetime] = None
    Name: Optional[str] = None
    Order: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.PortalLaunch.PortalLaunchWave"
