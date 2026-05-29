from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.sharepoint.fields.lookup_value import FieldLookupValue
from office365.sharepoint.principal.users.user import User


@dataclass
class FieldUserValue(FieldLookupValue):
    """Represents the value of a user fields for a list item."""

    Email: Optional[str] = None

    @staticmethod
    def from_user(user: User) -> "FieldUserValue":
        """
        Initialize field value from User
        :param User user: User object
        """
        return_type = FieldUserValue(-1)

        def _user_loaded():
            return_type.LookupId = user.id
            return_type.LookupValue = user.login_name

        user.ensure_properties(["Id", "LoginName"]).after_execute(lambda _: _user_loaded())
        return return_type
