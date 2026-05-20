from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SharingLinkAccessRequest(ClientValue):
    """
    Represents extended values to include in a request for access to an object exposed through a tokenized
    sharing link.

    Fields:
        ensureAccess: Indicates if the request to the tokenized sharing link grants perpetual access to
            the calling user.
        password: This value contains the password to be supplied to a tokenized sharing link for validation.
            This value is only needed if the link requires a password before granting access and the calling user
            does not currently have perpetual access through the tokenized sharing link.
            This value MUST be set to the correct password for the tokenized sharing link for the access granting
            operation to succeed. If the tokenized sharing link does not require a password or the calling user
            already has perpetual access through the tokenized sharing link, this value will be ignored.
    """

    ensureAccess: bool | None = None
    password: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingLinkAccessRequest"
