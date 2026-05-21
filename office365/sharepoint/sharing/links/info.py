from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sharing.invitation.link import LinkInvitation
from office365.sharepoint.sharing.principal import Principal


@dataclass
class SharingLinkInfo(ClientValue):
    """Specifies the information about the tokenized sharing link.

    :param bool allows_anonymous_access: Indicates whether the tokenized sharing link allows anonymous access.
    :param str application_id:
    :param str created: The UTC date/time string with complete representation for calendar date and time of day
         which represents the time and date of creation of the tokenized sharing link.
    :param Principal created_by: Indicates the principal who created the tokenized sharing link, or null if the
         created by value is not recorded.
    :param bool password_protected:
    :param list[LinkInvitation] invitations: This value contains the current membership list for principals
         that have been Invited to the tokenized sharing link.
    :param list[LinkInvitation] redeemed_users:
    :param Principal last_modified_by: Indicates the principal who last modified the tokenized sharing link.
         This value MUST be null if the last modified by value is not recorded.
    :param Principal password_last_modified_by:
    :param bool track_link_users:
    :param str share_token_string:
    """
    AllowsAnonymousAccess: bool | None = None
    ApplicationId: str | None = None
    Created: str | None = None
    CreatedBy: Principal = field(default_factory=Principal)
    PasswordProtected: bool | None = None
    Invitations: ClientValueCollection[LinkInvitation] = field(
        default_factory=lambda: ClientValueCollection(LinkInvitation)
    )
    RedeemedUsers: ClientValueCollection[LinkInvitation] = field(
        default_factory=lambda: ClientValueCollection(LinkInvitation)
    )
    LastModifiedBy: Principal = field(default_factory=Principal)
    PasswordLastModifiedBy: Principal = field(default_factory=Principal)
    TrackLinkUsers: bool | None = None
    ShareTokenString: str | None = None
    Url: str | None = None
    BlocksDownload: bool | None = None
    Description: str | None = None
    Embeddable: bool | None = None
    Expiration: str | None = None
    HasExternalGuestInvitees: bool | None = None
    IsActive: bool | None = None
    IsAddressBarLink: bool | None = None
    IsCreateOnlyLink: bool | None = None
    IsDefault: bool | None = None
    IsEditLink: bool | None = None
    IsEphemeral: bool | None = None
    IsFormsLink: bool | None = None
    IsMainLink: bool | None = None
    IsManageListLink: bool | None = None
    IsReviewLink: bool | None = None
    IsUnhealthy: bool | None = None
    LastModified: str | None = None
    LimitUseToApplication: bool | None = None
    LinkKind: int | None = None
    MeetingId: str | None = None
    MustAlwaysUseLink: bool | None = None
    PasswordLastModified: str | None = None
    RequiresPassword: bool | None = None
    RestrictedShareMembership: bool | None = None
    RestrictToExistingRelationships: bool | None = None
    Scope: int | None = None
    ShareId: str | None = None
    SharingLinkStatus: int | None = None

    def __str__(self):
        return self.Url or ""

    def __repr__(self):
        return self.Url or self.entity_type_name

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingLinkInfo"
