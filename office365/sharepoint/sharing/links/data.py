from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SharingLinkData(ClientValue):
    """
    This class stores basic overview information about the link URL, including limited data
    about the object the link URL refers to and any additional sharing link data if the link URL
    is a tokenized sharing link.
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
