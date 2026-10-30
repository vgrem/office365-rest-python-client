from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.common.qr_code import QrCode
    from office365.common.qr_pin import QrPin


class QrCodePinAuthenticationMethod(Entity):
    @odata(name="pin", navigation=True)
    @property
    def pin(self) -> QrPin:
        """Gets the pin property"""
        from office365.common.qr_pin import QrPin

        return self.properties.get("pin", QrPin(self.context, ResourcePath("pin", self.resource_path)))

    @odata(name="standardQRCode", navigation=True)
    @property
    def standard_qr_code(self) -> QrCode:
        """Gets the standardQRCode property"""
        from office365.common.qr_code import QrCode

        return self.properties.get(
            "standardQRCode", QrCode(self.context, ResourcePath("standardQRCode", self.resource_path))
        )

    @odata(name="temporaryQRCode", navigation=True)
    @property
    def temporary_qr_code(self) -> QrCode:
        """Gets the temporaryQRCode property"""
        from office365.common.qr_code import QrCode

        return self.properties.get(
            "temporaryQRCode", QrCode(self.context, ResourcePath("temporaryQRCode", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.QrCodePinAuthenticationMethod"
