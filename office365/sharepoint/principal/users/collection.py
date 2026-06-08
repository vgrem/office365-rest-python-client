from typing import Union

from typing_extensions import Self

from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.create_entity import CreateEntityQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.principal.users.user import User


class UserCollection(EntityCollection[User]):
    """Represents a collection of User resources in a SharePoint site."""

    def __init__(self, context, resource_path=None):
        """Initializes a new instance of the UserCollection class.

        Args:
            context: The client context.
            resource_path: The resource path for this collection.
        """
        super().__init__(context, User, resource_path)

    def add_user(self, user: Union[str, User]) -> User:
        """Creates a new user in the collection.

        Args:
            user: The user login name as string or User object.

        Returns:
            User: The newly created user object.

        """
        return_type = User(self.context)
        self.add_child(return_type)

        def _add_user(login_name: str):
            return_type.set_property("LoginName", login_name)
            qry = CreateEntityQuery(self, return_type, return_type)
            self.context.add_query(qry)

        if isinstance(user, User):
            user.ensure_property("LoginName").after_execute(
                lambda _: _add_user(user.login_name) if user.login_name is not None else None
            )
        else:
            _add_user(user)
        return return_type

    def get_by_principal_name(self, value: str) -> User:
        """Returns the user with the specified principal name.

        Args:
            value: The user principal name (e.g., user@domain.com).

        Returns:
            User: The user with the specified principal name.
        """
        return self.single(f"UserPrincipalName eq '{value}'")

    def get_by_email(self, email: str) -> User:
        """Returns the user with the specified email address.

        Args:
            email: The email address of the user.

        Returns:
            User: The user with the specified email address.
        """
        return User(
            self.context,
            ServiceOperationPath("GetByEmail", [email], self.resource_path),
        )

    def get_by_id(self, user_id: str) -> User:
        """Returns the user with the specified member identifier.

        Args:
            user_id (int): Specifies the member identifier.
        """
        return User(self.context, ServiceOperationPath("GetById", [user_id], self.resource_path))

    def get_by_login_name(self, login_name: str) -> User:
        """Retrieve User object by login name

        Args:
            login_name (str): A string that contains the login name of the user.
        """
        return User(
            self.context,
            ServiceOperationPath("GetByLoginName", [login_name], self.resource_path),
        )

    def remove_by_id(self, user_id: str) -> Self:
        """Retrieve User object by id

        Args:
            user_id (int): Specifies the member identifier.
        """
        qry = ServiceOperationQuery(self, "RemoveById", [user_id])
        self.context.add_query(qry)
        return self

    def remove_by_login_name(self, login_name: str) -> Self:
        """Remove User object by login name

        Args:
            login_name (str): A string that contains the username.
        """
        qry = ServiceOperationQuery(self, "RemoveByLoginName", [login_name])
        self.context.add_query(qry)
        return self
