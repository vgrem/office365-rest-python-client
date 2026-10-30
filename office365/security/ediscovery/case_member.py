from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.security.recipient_type import RecipientType


class EdiscoveryCaseMember(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="smtpAddress")
    @property
    def smtp_address(self) -> Optional[str]:
        """Gets the smtpAddress property"""
        return self.properties.get("smtpAddress", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.EdiscoveryCaseMember"

    @odata(name="recipientType")
    @property
    def recipient_type(self) -> RecipientType:
        """Gets the recipientType property"""
        from office365.security.recipient_type import RecipientType

        return self.properties.get("recipientType", RecipientType.user)
