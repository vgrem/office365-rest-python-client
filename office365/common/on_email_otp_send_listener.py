from __future__ import annotations

from office365.directory.identities.on_otp_send_handler import OnOtpSendHandler
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class OnEmailOtpSendListener(Entity):
    @odata(name="handler")
    @property
    def handler(self) -> OnOtpSendHandler:
        """Gets the handler property"""
        return self.properties.get("handler", OnOtpSendHandler())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnEmailOtpSendListener"
