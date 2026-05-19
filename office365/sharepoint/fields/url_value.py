from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class FieldUrlValue(ClientValue):
    """Specifies the hyperlink and the description values for FieldURL.

    Fields:
        Url (str | None): Specifies the URI. Its length MUST be equal to or less than 255. It MUST be one
             of the following: NULL, empty, an absolute URL, or a server-relative URL.
        Description (str | None): Specifies the description for the URI. Its length MUST be equal to or less than 255.
    """

    Url: str | None = None
    Description: str | None = None

    @property
    def entity_type_name(self):
        return "SP.FieldUrlValue"
