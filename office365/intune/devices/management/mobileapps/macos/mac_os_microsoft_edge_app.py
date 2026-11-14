from __future__ import annotations

from office365.intune.devices.management.mobileapps.microsoftedgechannel import MicrosoftEdgeChannel
from office365.intune.devices.management.mobileapps.mobile_app import MobileApp
from office365.runtime.types.odata_property import odata


class MacOSMicrosoftEdgeApp(MobileApp):
    @odata(name="channel")
    @property
    def channel(self) -> MicrosoftEdgeChannel:
        """Gets the channel property"""
        return self.properties.get("channel", MicrosoftEdgeChannel.dev)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MacOSMicrosoftEdgeApp"
