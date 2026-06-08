from __future__ import annotations

from typing import Optional

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.v3.static import StaticPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.directory.members_info import MembersInfo
from office365.sharepoint.directory.membership_result import MembershipResult
from office365.sharepoint.directory.my_groups_result import MyGroupsResult
from office365.sharepoint.directory.users.user import User
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection


class SPHelper(Entity):
    @property
    def resource_path(self):
        if self._resource_path is None:
            self._resource_path = StaticPath("SP.Directory.SPHelper")
        return self._resource_path

    @staticmethod
    def is_member_of(
        context: ClientContext,
        principal_name: str,
        group_id: str,
        result: Optional[ClientResult[bool]] = None,
    ) -> ClientResult[bool]:
        """Args:
        principal_name (str): User principal name
        group_id (str): Group id
        context (office365.sharepoint.client_context.ClientContext): SharePoint context
        result (ClientResult or None): Client result
        """
        if result is None:
            result = ClientResult(context)
        payload = {"principalName": principal_name, "groupId": group_id}
        qry = ServiceOperationQuery(SPHelper(context), "IsMemberOf", None, payload, None, result, True)
        context.add_query(qry)
        return result

    @staticmethod
    def check_site_availability(context: ClientContext, site_url: str) -> ClientResult[bool]:
        """ """
        return_type = ClientResult(context)
        qry = ServiceOperationQuery(
            SPHelper(context),
            "CheckSiteAvailability",
            None,
            {"siteUrl": site_url},
            None,
            return_type,
        )
        qry.static = True
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_membership(context, user_id):
        """Args:
        context (office365.sharepoint.client_context.ClientContext): SharePoint client context
        user_id (str): User's identifier
        """
        payload = {"userId": user_id}
        return_type = MembershipResult(context)
        qry = ServiceOperationQuery(SPHelper(context), "GetMembership", None, payload, None, return_type, True)
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_members_info(context, group_id, row_limit, return_type=None):
        """Args:
        context (office365.sharepoint.client_context.ClientContext): SharePoint context
        group_id (str): User's login
        row_limit (int): Result offset
        return_type (MembersInfo): Result
        """
        if return_type is None:
            return_type = MembersInfo(context)
        payload = {
            "groupId": group_id,
            "rowLimit": row_limit,
        }
        qry = ServiceOperationQuery(SPHelper(context), "GetMembersInfo", None, payload, None, return_type, True)
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_my_groups(context, logon_name, offset, length, return_type=None):
        """Retrieves information about groups that a user belongs to.

        Args:
            context (office365.sharepoint.client_context.ClientContext): SharePoint context
            logon_name (str): User's login
            offset (int): Result offset
            length (int): Results count
            return_type (MyGroupsResult): return type
        """
        if return_type is None:
            return_type = MyGroupsResult(context)
        payload = {"logOnName": logon_name, "offset": offset, "len": length}
        qry = ServiceOperationQuery(SPHelper(context), "GetMyGroups", None, payload, None, return_type, True)
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_members(context, group_id, return_type=None):
        """Args:
        group_id (str): Group identifier
        context (office365.sharepoint.client_context.ClientContext): SharePoint context
        return_type (EntityCollection or None): Returns members
        """
        if return_type is None:
            return_type = EntityCollection(context, User)
        qry = ServiceOperationQuery(SPHelper(context), "GetMembers", [group_id], None, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_owners(
        context: ClientContext,
        group_id: str,
        return_type: Optional[EntityCollection[User]] = None,
    ) -> EntityCollection[User]:
        """Args:
        group_id (str): Group identifier
        context (office365.sharepoint.client_context.ClientContext): SharePoint context
        return_type (EntityCollection or None): Returns members
        """
        if return_type is None:
            return_type = EntityCollection(context, User)
        qry = ServiceOperationQuery(SPHelper(context), "GetOwners", [group_id], None, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type

    @staticmethod
    def remove_external_members(context: ClientContext, group_id: str) -> SPHelper:
        """Args:
        group_id (str): Group identifier
        context (office365.sharepoint.client_context.ClientContext): SharePoint context
        """
        binding_type = SPHelper(context)
        qry = ServiceOperationQuery(binding_type, "RemoveExternalMembers", [group_id], is_static=True)
        context.add_query(qry)
        return binding_type

    @property
    def entity_type_name(self):
        return "SP.Directory.SPHelper"
