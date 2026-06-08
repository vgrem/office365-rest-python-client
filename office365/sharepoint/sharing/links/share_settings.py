from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sharing.principal import Principal


@dataclass
class ShareLinkSettings(ClientValue):
    """Represents the settings the retrieval or creation/update of a tokenized sharing link

    Args:
        allow_anonymous_access (bool): Indicates if the tokenized sharing link supports anonymous access. This value is optional and defaults to false for Flexible links (section 3.2.5.315.1.7) and is ignored for other link kinds.
        application_link (bool):
        link_kind (int): The kind of the tokenized sharing link to be created/updated or retrieved. This value MUST NOT be set to Uninitialized (section 3.2.5.315.1.1) nor Direct (section 3.2.5.315.1.2)
        password (str): Optional password value to apply to the tokenized sharing link, if it can support password protection. If this value is null or empty when the updatePassword parameter is set, any existing password on the tokenized sharing link MUST be cleared. Any other value will be applied to the tokenized sharing link as a password setting.
        password_protected (bool):
        role (int): The role to be used for the tokenized sharing link. This is required for Flexible links and ignored for all other kinds.
        track_link_users (bool):
        share_id (str): The optional unique identifier of an existing section tokenized sharing link to be retrieved and updated if necessary.
        update_password (bool):
    """

    allowAnonymousAccess: bool | None = None
    applicationLink: bool | None = None
    linkKind: int | None = None
    expiration: str | None = None
    password: str | None = None
    password_protected: bool | None = field(default=None, repr=False)
    passwordProtected: bool | None = field(init=False, default=None)
    role: int | None = None
    shareId: str | None = None
    trackLinkUsers: bool | None = None
    updatePassword: bool | None = None
    description: str | None = None
    embeddable: bool | None = None
    inviteesToRemove: ClientValueCollection[Principal] = field(default_factory=lambda: ClientValueCollection(Principal))
    limitUseToApplication: bool | None = None
    nav: str | None = None
    nonDefaultLink: bool | None = None
    restrictShareMembership: bool | None = None
    restrictToExistingRelationships: bool | None = None
    scope: int | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.ShareLinkSettings"

    def __post_init__(self):
        self.passwordProtected = True if self.password else self.password_protected
