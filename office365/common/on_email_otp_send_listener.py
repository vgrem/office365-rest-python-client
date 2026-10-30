from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identities.on_otp_send_handler import OnOtpSendHandler


class OnEmailOtpSendListener(Entity):
    @odata(name="handler")
    @property
    def handler(self) -> OnOtpSendHandler:
        """Gets the handler property"""
        from office365.directory.identities.on_otp_send_handler import OnOtpSendHandler

        return self.properties.get("handler", OnOtpSendHandler())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnEmailOtpSendListener"
