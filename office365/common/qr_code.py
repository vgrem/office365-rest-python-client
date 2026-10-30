from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.authentication.qr_code_image_details import (
        QrCodeImageDetails,
    )


class QrCode(Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="expireDateTime")
    @property
    def expire_date_time(self) -> Optional[datetime]:
        """Gets the expireDateTime property"""
        return self.properties.get("expireDateTime", datetime.min)

    @odata(name="image")
    @property
    def image(self) -> QrCodeImageDetails:
        """Gets the image property"""
        from office365.directory.authentication.qr_code_image_details import (
            QrCodeImageDetails,
        )

        return self.properties.get("image", QrCodeImageDetails())

    @odata(name="lastUsedDateTime")
    @property
    def last_used_date_time(self) -> Optional[datetime]:
        """Gets the lastUsedDateTime property"""
        return self.properties.get("lastUsedDateTime", datetime.min)

    @odata(name="startDateTime")
    @property
    def start_date_time(self) -> Optional[datetime]:
        """Gets the startDateTime property"""
        return self.properties.get("startDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.QrCode"
