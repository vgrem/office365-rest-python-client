from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.calendar.email_address import EmailAddress
from office365.runtime.client_value import ClientValue
from office365.runtime.types.odata_property import Compare, odata


@dataclass
class Recipient(ClientValue):
    """The recipient of an event, message, or group post."""

    emailAddress: EmailAddress = field(
        default_factory=EmailAddress, metadata=odata("emailAddress", compare=Compare(key=True))
    )

    @staticmethod
    def from_email(value: str | EmailAddress) -> Recipient:
        if isinstance(value, EmailAddress):
            return Recipient(value)
        return Recipient(EmailAddress(value))

    @property
    def entity_type_name(self) -> str | None:
        return None

    def __repr__(self) -> str:
        return repr(self.emailAddress)
