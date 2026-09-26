from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class QuotaMigrationApi(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.QuotaManagement.Consumer.QuotaMigrationApi"

    def migrate_quota(self, is_max_quota_call: bool) -> ClientResult[str]:
        """MigrateQuota operation.

        Args:
            is_max_quota_call (bool): IsMaxQuotaCall parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(self, "MigrateQuota", None, {"IsMaxQuotaCall": is_max_quota_call}, None, return_type)
        self.context.add_query(qry)
        return return_type
