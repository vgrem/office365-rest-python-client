from __future__ import annotations

from typing import TYPE_CHECKING

from office365.runtime.client_object import ClientObject
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.v3.static import StaticPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.userprofiles.user_profile import UserProfile

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class ProfileLoader(ClientObject):
    """The ProfileLoader class provides access to the current user's profile."""

    def __init__(self, context):
        super().__init__(
            context, StaticPath("SP.UserProfiles.ProfileLoader.GetProfileLoader")
        )

    @staticmethod
    def get_profile_loader(context: ClientContext) -> ProfileLoader:
        """
        The GetProfileLoader method returns a profile loader.
        """
        return_type = ProfileLoader(context)
        qry = ServiceOperationQuery(
            return_type, "GetProfileLoader", None, None, None, return_type, True
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_owner_user_profile(context: ClientContext) -> UserProfile:
        """
        Gets the user profile for the Site owner.
        """
        return_type = UserProfile(context)
        qry = ServiceOperationQuery(
            ProfileLoader(context),
            "GetOwnerUserProfile",
            None,
            None,
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type

    def get_user_profile(self) -> UserProfile:
        """The GetUserProfile method returns the user profile for the current user."""
        result = UserProfile(
            self.context, ResourcePath("GetUserProfile", self.resource_path)
        )
        qry = ServiceOperationQuery(self, "GetUserProfile", None, None, None, result)
        self.context.add_query(qry)
        return result

    @property
    def entity_type_name(self):
        return "SP.UserProfiles.ProfileLoader"
