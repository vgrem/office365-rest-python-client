from typing_extensions import Self

from office365.count_collection import CountCollection
from office365.directory.users.profile import UserProfile
from office365.directory.users.user import User
from office365.permissions import require_permission
from office365.runtime.odata.literals import escape_odata_string
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.create_entity import CreateEntityQuery


class UserCollection(CountCollection[User]):
    """User's collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, User, resource_path)

    def get_by_principal_name(self, name: str) -> User:
        """Retrieves User by principal name

        Args:
            name (str): User principal name
        """
        return User(self.context, ResourcePath(name, self.resource_path))

    def find_by_mail(self, user_mail: str, *, required: bool = False) -> User:
        """Look up a user by their ``mail`` address.

        Unlike :meth:`get_by_principal_name` (which addresses the user directly
        and raises on a 404), this filters ``GET /users?$filter=mail eq '...'``.
        Deferred — run with ``execute_query()``. Tolerant by default: the
        returned user is left uninitialized when no user has that mail (check
        :attr:`~office365.runtime.client_object.ClientObject.is_loaded`). Pass
        ``required=True`` to raise instead (or on an ambiguous match).

        Args:
            user_mail (str): The user's ``mail`` address
            required (bool): Raise on a missing or ambiguous match when ``True``
        """
        return self._find_by_filter(f"mail eq '{escape_odata_string(user_mail)}'", required=required)

    def get_unlicensed(self) -> Self:
        """Get users holding no licence — a server-side filter.

        ``assignedLicenses`` is derived and no user projection carries it, so filtering it in the
        client would call every user unlicensed. This asks the service instead
        (``$filter=assignedLicenses/$count eq 0``); that advanced query needs
        ``ConsistencyLevel: eventual``, which :meth:`consistency_level` sets.
        """
        return self.consistency_level().filter("assignedLicenses/$count eq 0")

    def get_licensed(self) -> Self:
        """Get users holding at least one licence; see :meth:`get_unlicensed`."""
        return self.consistency_level().filter("assignedLicenses/$count ne 0")

    @require_permission(
        delegated=["User.ReadWrite.All", "Directory.ReadWrite.All"],
        application=["User.ReadWrite.All", "Directory.ReadWrite.All"],
    )
    def add(self, user_properties: UserProfile) -> User:
        """Create a new user.

        Args:
            user_properties (office365.directory.users.profile.UserProfile):
        """
        return_type = User(self.context)
        qry = CreateEntityQuery(self, user_properties, return_type)
        self.context.add_query(qry)
        self.add_child(return_type)
        return return_type
