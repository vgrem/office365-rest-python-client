from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.sharepoint.alerts.collection import AlertCollection
from office365.sharepoint.principal.principal import Principal
from office365.sharepoint.principal.users.id_info import UserIdInfo
from office365.sharepoint.userprofiles.person_properties import PersonProperties

if TYPE_CHECKING:
    from office365.sharepoint.sites.site import Site


class User(Principal):
    """Represents a user in Microsoft SharePoint Foundation. A user is a type of SP.Principal.

    ``SP.User`` carries thirteen properties and two links, and that is all it carries: the profile
    fields a *user profile* answers -- ``aboutMe``, ``skills``, ``hireDate`` -- are not among them,
    and the service drops such a name from ``$select`` silently, leaving an empty payload.  Read them
    from :class:`office365.sharepoint.directory.users.user.User` (``SP.Directory.User``) or through
    :meth:`~office365.sharepoint.userprofiles.people_manager.PeopleManager.get_user_profile_properties`.
    """

    def get_personal_site(self) -> "Site":
        """Get personal site for a user"""
        from office365.sharepoint.sites.site import Site

        return_type = Site(self.context)

        def _person_props_loaded(person_props: PersonProperties) -> None:
            return_type.set_property("__siteUrl", person_props.personal_url)

        def _get_properties_for():
            assert self.login_name is not None
            self.context.people_manager.get_properties_for(self.login_name).after_execute(_person_props_loaded)

        self.ensure_property("LoginName").after_execute(lambda _: _get_properties_for())
        return return_type

    def get_recent_files(self, top: int = 100) -> ClientResult[str]:
        """"""
        from office365.sharepoint.files.recent_file_collection import RecentFileCollection

        return_type = RecentFileCollection.get_recent_files(self.context, top)
        return return_type

    def expire(self) -> Self:
        """"""
        qry = ServiceOperationQuery(self, "Expire")
        self.context.add_query(qry)
        return self

    @odata(name="AadObjectId")
    @property
    def aad_object_id(self) -> UserIdInfo:
        """Gets the information of the user that contains the user's name identifier and the issuer of the
        user's name identifier."""
        return self.properties.get("AadObjectId", UserIdInfo())

    @odata(name="Alerts", navigation=True)
    @property
    def alerts(self) -> AlertCollection:
        """Gets site alerts for this user."""
        return self.properties.get("Alerts", AlertCollection(self.context, ResourcePath("Alerts", self.resource_path)))

    @odata(name="Groups", navigation=True)
    @property
    def groups(self):
        """Gets a collection of group objects that represents all of the groups for the user."""
        from office365.sharepoint.principal.groups.collection import GroupCollection

        return self.properties.get("Groups", GroupCollection(self.context, ResourcePath("Groups", self.resource_path)))

    @odata(name="IsSiteAdmin")
    @property
    def is_site_admin(self) -> Optional[bool]:
        """Gets a Boolean value that specifies whether the user is a site collection administrator."""
        return self.properties.get("IsSiteAdmin", None)

    @odata(name="UserId")
    @property
    def user_id(self) -> UserIdInfo:
        """Gets the information of the user that contains the user's name identifier and the issuer of the
        user's name identifier."""
        return self.properties.get("UserId", UserIdInfo())

    @odata(name="Email")
    @property
    def email(self) -> Optional[str]:
        """
        Specifies the e-mail address of the user.
        It MUST NOT be NULL. Its length MUST be equal to or less than 255.
        """
        return self.properties.get("Email", None)

    @odata(name="EmailWithFallback")
    @property
    def email_with_fallback(self) -> Optional[str]:
        return self.properties.get("EmailWithFallback", None)

    @odata(name="Expiration")
    @property
    def expiration(self) -> Optional[str]:
        return self.properties.get("Expiration", None)

    @odata(name="IsEmailAuthenticationGuestUser")
    @property
    def is_email_authentication_guest_user(self) -> Optional[bool]:
        """
        Indicates whether the User is a share by email guest user using time of access authentication.
        If this instance is an email authentication guest user, this value MUST be true, otherwise it MUST be false.
        """
        return self.properties.get("IsEmailAuthenticationGuestUser", None)

    @odata(name="IsShareByEmailGuestUser")
    @property
    def is_share_by_email_guest_user(self) -> Optional[bool]:
        """
        Gets a value indicating whether this User is a share by email guest user.
        If this instance is a share by email guest user, it's true; otherwise, false.
        """
        return self.properties.get("IsShareByEmailGuestUser", None)

    @odata(name="UserPrincipalName")
    @property
    def user_principal_name(self) -> Optional[str]:
        """User principal name of the user that initiated the sign-in."""
        return self.properties.get("UserPrincipalName", None)

    @property
    def entity_type_name(self) -> str:
        return "SP.User"

    @odata(name="HexCid")
    @property
    def hex_cid(self) -> Optional[str]:
        """Gets the HexCid property"""
        return self.properties.get("HexCid", None)

    @odata(name="UserIdentityType")
    @property
    def user_identity_type(self) -> Optional[int]:
        """Gets the UserIdentityType property"""
        return self.properties.get("UserIdentityType", None)
