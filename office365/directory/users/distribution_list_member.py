from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.security.recipient_type import RecipientType

if TYPE_CHECKING:
    from office365.outlook.contacts.contact import Contact


class DistributionListMember(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="memberId")
    @property
    def member_id(self) -> Optional[str]:
        """Gets the memberId property"""
        return self.properties.get("memberId", None)

    @odata(name="type")
    @property
    def type(self) -> RecipientType:
        """Gets the type property"""
        return self.properties.get("type", RecipientType.user)

    @odata(name="contact", navigation=True)
    @property
    def contact(self) -> Contact:
        """Gets the contact property"""
        from office365.outlook.contacts.contact import Contact

        return self.properties.get("contact", Contact(self.context, ResourcePath("contact", self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DistributionListMember"
