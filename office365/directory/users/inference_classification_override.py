from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.outlook.mail.inferenceclassificationtype import InferenceClassificationType
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.outlook.calendar.email_address import EmailAddress


class InferenceClassificationOverride(Entity):
    @odata(name="classifyAs")
    @property
    def classify_as(self) -> InferenceClassificationType:
        """Gets the classifyAs property"""
        return self.properties.get("classifyAs", InferenceClassificationType.focused)

    @odata(name="senderEmailAddress")
    @property
    def sender_email_address(self) -> EmailAddress:
        """Gets the senderEmailAddress property"""
        from office365.outlook.calendar.email_address import EmailAddress

        return self.properties.get("senderEmailAddress", EmailAddress())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.InferenceClassificationOverride"
