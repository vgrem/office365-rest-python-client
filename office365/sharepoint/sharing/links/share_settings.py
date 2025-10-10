from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sharing.principal import Principal


class ShareLinkSettings(ClientValue):
    """Represents the settings the retrieval or creation/update of a tokenized sharing link"""

    def __init__(
        self,
        allow_anonymous_access=None,
        application_link=None,
        link_kind=None,
        expiration=None,
        password=None,
        password_protected=None,
        role=None,
        track_link_users=None,
        share_id=None,
        update_password=None,
        description: str = None,
        embeddable: bool = None,
        invitees_to_remove: ClientValueCollection[Principal] = ClientValueCollection(
            Principal
        ),
        limit_use_to_application: bool = None,
        nav: str = None,
        non_default_link: bool = None,
        restrict_share_membership: bool = None,
        restrict_to_existing_relationships: bool = None,
        scope: int = None,
    ):
        """
        :param bool allow_anonymous_access: Indicates if the tokenized sharing link supports anonymous access.
             This value is optional and defaults to false for Flexible links (section 3.2.5.315.1.7) and is ignored
             for other link kinds.
        :param bool application_link:
        :param int link_kind: The kind of the tokenized sharing link to be created/updated or retrieved.
            This value MUST NOT be set to Uninitialized (section 3.2.5.315.1.1) nor Direct (section 3.2.5.315.1.2)
        :param str password: Optional password value to apply to the tokenized sharing link, if it can support password
            protection. If this value is null or empty when the updatePassword parameter is set, any existing password
            on the tokenized sharing link MUST be cleared. Any other value will be applied to the tokenized sharing link
            as a password setting.
        :param bool password_protected:
        :param int role: The role to be used for the tokenized sharing link. This is required for Flexible links
            and ignored for all other kinds.
        :param bool track_link_users:
        :param str share_id: The optional unique identifier of an existing section tokenized sharing link to be
             retrieved and updated if necessary.
        :param bool update_password:
        """
        self.allowAnonymousAccess = allow_anonymous_access
        self.applicationLink = application_link
        self.linkKind = link_kind
        self.expiration = expiration
        self.password = password
        self.passwordProtected = True if password else password_protected
        self.role = role
        self.shareId = share_id
        self.trackLinkUsers = track_link_users
        self.updatePassword = update_password
        self.description = description
        self.embeddable = embeddable
        self.inviteesToRemove = invitees_to_remove
        self.limitUseToApplication = limit_use_to_application
        self.nav = nav
        self.nonDefaultLink = non_default_link
        self.restrictShareMembership = restrict_share_membership
        self.restrictToExistingRelationships = restrict_to_existing_relationships
        self.scope = scope

    @property
    def entity_type_name(self):
        return "SP.Sharing.ShareLinkSettings"
