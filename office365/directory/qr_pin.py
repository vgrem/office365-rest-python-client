from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class QrPin(Entity):
    @odata(name="code")
    @property
    def code(self) -> Optional[str]:
        """Gets the code property"""
        return self.properties.get("code", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="forceChangePinNextSignIn")
    @property
    def force_change_pin_next_sign_in(self) -> Optional[bool]:
        """Gets the forceChangePinNextSignIn property"""
        return self.properties.get("forceChangePinNextSignIn", None)

    @odata(name="updatedDateTime")
    @property
    def updated_date_time(self) -> Optional[datetime]:
        """Gets the updatedDateTime property"""
        return self.properties.get("updatedDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.QrPin"
