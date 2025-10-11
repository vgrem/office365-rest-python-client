from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.v3.static import StaticPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.tenant.administration.groups.info import GroupInfo


class SPOGroup(Entity):
    """ """

    def __init__(self, context, resource_path=None):
        if resource_path is None:
            resource_path = StaticPath("Microsoft.Online.SharePoint.TenantAdministration.SPOGroup")
        super(SPOGroup, self).__init__(context, resource_path)

    def add_as_group_owner_and_member(self, group_id: str, user_id: str, user_principal_name: str) -> Self:
        """ """
        payload = {
            "groupId": group_id,
            "userId": user_id,
            "userPrincipalName": user_principal_name,
        }
        qry = ServiceOperationQuery(self, "AddAsGroupOwnerAndMember", None, payload, None)
        self.context.add_query(qry)
        return self

    def get_group_info(self, group_id):
        """"""
        return_type = ClientResult(self.context, GroupInfo())
        payload = {"groupId": group_id}
        qry = ServiceOperationQuery(self, "GetGroupInfo", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOGroup"
