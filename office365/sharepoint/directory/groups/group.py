from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.directory.helper import SPHelper
from office365.sharepoint.directory.members_info import MembersInfo
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.principal.principal import Principal

if TYPE_CHECKING:
    from office365.sharepoint.directory.users.user import User


class Group(Entity):
    """Represents a directory group in SharePoint."""

    def get_members_info(self, row_limit: int) -> MembersInfo:
        """Gets information about the group members.

        Args:
            row_limit: Maximum number of members to return

        Returns:
            MembersInfo object containing member information
        """
        return_type = MembersInfo(self.context)

        def _get_members_info():
            from office365.sharepoint.directory.helper import SPHelper

            SPHelper.get_members_info(self.context, self.properties["Id"], row_limit, return_type)

        self.ensure_property("Id").after_execute(lambda _: _get_members_info())
        return return_type

    def get_members(self):
        """Gets the group's members.

        Returns:
            Collection of User objects representing group members
        """
        from office365.sharepoint.directory.users.user import User

        return_type = EntityCollection(self.context, User)

        def _group_loaded():
            SPHelper.get_members(self.context, self.properties["Id"], return_type)

        self.ensure_property("Id").after_execute(lambda _: _group_loaded())
        return return_type

    def get_owners(self) -> EntityCollection[User]:
        """Gets the group's owners.

        Returns:
            Collection of User objects representing group owners
        """
        from office365.sharepoint.directory.users.user import User

        return_type = EntityCollection[User](self.context, User)

        def _get_owners():
            SPHelper.get_owners(self.context, self.properties["Id"], return_type)

        self.ensure_property("Id").after_execute(lambda _: _get_owners())
        return return_type

    @property
    def entity_type_name(self):
        return "SP.Directory.Group"

    @property
    def allow_members_edit_membership(self) -> Optional[bool]:
        """Gets the AllowMembersEditMembership property"""
        return self.properties.get("AllowMembersEditMembership", None)

    @property
    def allow_request_to_join_leave(self) -> Optional[bool]:
        """Gets the AllowRequestToJoinLeave property"""
        return self.properties.get("AllowRequestToJoinLeave", None)

    @property
    def auto_accept_request_to_join_leave(self) -> Optional[bool]:
        """Gets the AutoAcceptRequestToJoinLeave property"""
        return self.properties.get("AutoAcceptRequestToJoinLeave", None)

    @property
    def can_current_user_edit_membership(self) -> Optional[bool]:
        """Gets the CanCurrentUserEditMembership property"""
        return self.properties.get("CanCurrentUserEditMembership", None)

    @property
    def can_current_user_manage_group(self) -> Optional[bool]:
        """Gets the CanCurrentUserManageGroup property"""
        return self.properties.get("CanCurrentUserManageGroup", None)

    @property
    def can_current_user_view_membership(self) -> Optional[bool]:
        """Gets the CanCurrentUserViewMembership property"""
        return self.properties.get("CanCurrentUserViewMembership", None)

    @property
    def contains_current_user(self) -> Optional[bool]:
        """Gets the ContainsCurrentUser property"""
        return self.properties.get("ContainsCurrentUser", None)

    @property
    def description(self) -> Optional[str]:
        """Gets the Description property"""
        return self.properties.get("Description", None)

    @property
    def only_allow_members_view_membership(self) -> Optional[bool]:
        """Gets the OnlyAllowMembersViewMembership property"""
        return self.properties.get("OnlyAllowMembersViewMembership", None)

    @property
    def owner_title(self) -> Optional[str]:
        """Gets the OwnerTitle property"""
        return self.properties.get("OwnerTitle", None)

    @property
    def request_to_join_leave_email_setting(self) -> Optional[str]:
        """Gets the RequestToJoinLeaveEmailSetting property"""
        return self.properties.get("RequestToJoinLeaveEmailSetting", None)

    @property
    def owner(self) -> Principal:
        """Gets the Owner property"""
        return self.properties.get("Owner", Principal(self.context, ResourcePath("Owner", self.resource_path)))

    @property
    def users(self) -> EntityCollection[User]:
        """Gets the Users property"""
        return self.properties.get(
            "Users", EntityCollection[User](self.context, User, ResourcePath("Users", self.resource_path))
        )

    def set_user_as_owner(self, owner_id: int) -> Self:
        """SetUserAsOwner operation.

        Args:
            owner_id (int): ownerId parameter
        """
        qry = ServiceOperationQuery(self, "SetUserAsOwner", None, {"ownerId": owner_id}, None, None)
        self.context.add_query(qry)
        return self
