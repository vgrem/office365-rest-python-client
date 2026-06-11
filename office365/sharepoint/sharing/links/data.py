from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SharingLinkData(ClientValue):
    """
    This class stores basic overview information about the link URL, including limited data
    about the object the link URL refers to and any additional sharing link data if the link URL
    is a tokenized sharing link.

    Fields:
        Expiration: The UTC date/time string with complete representation for calendar date and time of day
            which represents the time and date of expiry for the tokenized sharing link
            (i.e. is not accessible anymore).
        HasExternalGuestInvitees: Boolean indicating whether the link URL is a tokenized sharing link that has
            any external guest invitees (external users explicitly invited by email address).
        IsAnonymous: Boolean indicating if the link is anonymously accessible.
        IsFormsLink: Indicates if the link URL is a tokenized sharing link that supports forms sharing.
            This is limited to only tokenized sharing links generated with the Excel Survey feature.
        IsReviewLink: Indicates if the link URL is a tokenized sharing link that supports review operations.
            This value MUST be true only if the link URL is a tokenized sharing link which is configured to
            support access with the review role, otherwise this MUST be false.
        IsSharingLink: Indicates if the link URL is a tokenized sharing link. This value MUST be true only if
            the link URL is a tokenized sharing link, otherwise this MUST be false.
        IsWritable: Indicates if the link URL is a tokenized sharing link that supports write/edit operations.
            This value MUST be true only if the link URL is a tokenized sharing link which is configured to
            support access with the edit role, otherwise this MUST be false.
        LinkKind: The kind of link that the link URL refers to.
        ObjectType: The type of object the link URL refers to.
    """

    BlocksDownload: bool | None = None
    Description: str | None = None
    Embeddable: bool | None = None
    Expiration: str | None = None
    HasExternalGuestInvitees: bool | None = None
    IsAnonymous: bool | None = None
    IsCreateOnlyLink: bool | None = None
    IsFormsLink: bool | None = None
    IsManageListLink: bool | None = None
    IsOriginatedFromSharingFlow: bool | None = None
    IsReviewLink: bool | None = None
    IsSharingLink: bool | None = None
    IsWritable: bool | None = None
    LinkKind: int | None = None
    ObjectType: int | None = None
    IsAddressBarLink: bool | None = None
    ObjectUniqueId: str | None = None
    RequiresPassword: bool | None = None
    RestrictedShareMembership: bool | None = None
    RestrictToExistingRelationships: bool | None = None
    ShareId: str | None = None
    TrackLinkUsers: bool | None = None
    IsMainLink: bool | None = None
    LinkScope: int | None = None
