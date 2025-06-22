from __future__ import annotations

from typing import TYPE_CHECKING

from office365.runtime.client_result import ClientResult
from office365.runtime.client_value import ClientValue
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class SystemSiteLockExpirationResult(ClientValue):
    """"""

    def __init__(self, error=None, expiration=None):
        self.Error = error
        self.Expiration = expiration


class SiteMoveService(Entity):
    """ """

    def __init__(
        self,
        context: ClientContext,
        site_id: str,
        site_subscription_id: str = None,
        source_database_id: str = None,
        target_database_id: str = None,
    ) -> None:
        """"""
        static_path = ServiceOperationPath(
            "Microsoft.SharePoint.Administration.SiteMove.Service.SiteMoveService",
            {
                "siteId": site_id,
                "siteSubscriptionId": site_subscription_id,
                "sourceDatabaseId": source_database_id,
                "targetDatabaseId": target_database_id,
            },
        )
        super(SiteMoveService, self).__init__(context, static_path)

    def acquire_system_site_lock(
        self, lock_requestor: str, lock_type: int, lease_duration_in_minutes: int
    ) -> ClientResult[SystemSiteLockExpirationResult]:
        """"""
        return_type = ClientResult(self.context, SystemSiteLockExpirationResult())
        payload = {
            "lockRequestor": lock_requestor,
            "lockType": lock_type,
            "leaseDurationInMinutes": lease_duration_in_minutes,
        }
        qry = ServiceOperationQuery(
            self,
            "AcquireSystemSiteLock",
            None,
            payload,
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.SiteMove.Service.SiteMoveService"
