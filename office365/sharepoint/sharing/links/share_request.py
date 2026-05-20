from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.emaildata import EmailData
from office365.sharepoint.sharing.links.share_settings import ShareLinkSettings


@dataclass
class ShareLinkRequest(ClientValue):
    """
    Represents a request for the retrieval or creation of a tokenized sharing link.

    Fields:
        linkKind: The kind of the tokenized sharing link to be created/updated or retrieved.
        expiration: A date/time string for which the format conforms to the ISO 8601:2004(E) complete representation
            for calendar date and time of day and which represents the time and date of expiry for the tokenized
            sharing link. Both the minutes and hour value MUST be specified for the difference between the local
            and UTC time. Midnight is represented as 00:00:00. A null value indicates no expiry. This value is only
            applicable to tokenized sharing links that are anonymous access links.
        peoplePickerInput: A string of JSON serialized data representing users in people picker format.
            This value specifies a list of identities that will be pre-granted access through the tokenized sharing
            link and optionally sent an e-mail notification.
            If this value is null or empty, no identities will be will be pre-granted access through the tokenized
            sharing link and no notification email will be sent.
        settings: The settings for the tokenized sharing link to be created/updated.
        createLink: Indicates whether the operation attempts to create the tokenized sharing link based on the
            requested settings if it does not currently exist.
            If set to true, the operation will attempt to retrieve an existing tokenized sharing link that matches
            the requested settings and failing that will attempt to create a new tokenized sharing link based on the
            requested settings. If false, the operation will attempt to retrieve an existing tokenized sharing link
            that matches the requested settings and failing that will terminate the operation.
    """

    linkKind: int | None = None
    expiration: str | None = None
    peoplePickerInput: str | None = None
    settings: ShareLinkSettings | None = None
    createLink: bool = True
    emailData: EmailData = field(default_factory=EmailData)

    @property
    def entity_type_name(self):
        return "SP.Sharing.ShareLinkRequest"
