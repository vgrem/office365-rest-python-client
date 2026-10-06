from typing_extensions import Self

from office365.count_collection import CountCollection
from office365.directory.permissions.require_permission import require_permission
from office365.directory.users.profile import UserProfile
from office365.directory.users.user import User
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

    def get_by_mail(self, user_mail: str) -> User:
        """Queue a lookup of a user by their ``mail`` address.

        Unlike :meth:`get_by_principal_name` (which addresses the user directly
        and raises on a 404), this filters ``GET /users?$filter=mail eq '...'``
        and tolerates a missing address. Deferred — run with
        ``execute_query()``; the returned user is left uninitialized when no
        user has that mail (check
        :attr:`~office365.runtime.client_object.ClientObject.is_loaded`).

        Args:
            user_mail (str): The user's ``mail`` address
        """
        escaped = user_mail.replace("'", "''")
        return self.first_or_none(f"mail eq '{escaped}'")

    def get_unlicensed(self) -> Self:
        """Get users with no assigned licenses (client-side filter)."""

        def _loaded(col: UserCollection):
            for user in col:
                if user.assigned_licenses:
                    self.remove_child(user)

        self.ensure_property("assignedLicenses").after_execute(_loaded)
        return self

    def get_licensed(self):
        """Get users with assigned licenses (client-side filter)."""

        def _loaded(col: UserCollection):
            for user in col:
                if not user.assigned_licenses:
                    self.remove_child(user)

        self.ensure_property("assignedLicenses").after_execute(_loaded)
        return self

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
