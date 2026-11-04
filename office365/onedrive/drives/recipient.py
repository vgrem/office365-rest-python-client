from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class DriveRecipient(ClientValue):
    """
    The DriveRecipient resource represents a person, group, or other recipient to
    share with using the invite action.
    """

    alias: str | None = None
    email: str | None = None
    objectId: str | None = None

    @staticmethod
    def from_email(value: str):
        """Creates Drive recipient from email address

        Args:
            value (str):
        """
        return DriveRecipient(email=value)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DriveRecipient"
