from __future__ import annotations

from typing import TYPE_CHECKING

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class PolicyLicenseUtilities(Entity):
    """"""

    @staticmethod
    def check_tenant_m365_copilot_business_chat_license(
        context: ClientContext, return_type: ClientResult[bool] = None
    ) -> ClientResult[bool]:
        """"""
        if return_type is None:
            return_type = ClientResult(context, bool())
        qry = ServiceOperationQuery(
            PolicyLicenseUtilities(context),
            "CheckTenantM365CopilotBusinessChatLicense",
            None,
            None,
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "SP.Utilities.PolicyLicenseUtilities"
