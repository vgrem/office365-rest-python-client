from __future__ import annotations

from office365.education.contactrelationship import ContactRelationship
from office365.runtime.client_value import ClientValue


class RelatedContact(ClientValue):
    accessConsent: bool | None = None
    displayName: str | None = None
    emailAddress: str | None = None
    mobilePhone: str | None = None
    relationship: ContactRelationship = ContactRelationship.parent

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RelatedContact"
