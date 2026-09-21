from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class TenantRecycleBinInfoProvider(Entity):
    """ """

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Client.Search.Administration.TenantRecycleBinInfoProvider"

    def disable_recycle_bin_discoverability_for_tenant(self) -> ClientResult[bool]:
        """DisableRecycleBinDiscoverabilityForTenant operation."""
        return_type = ClientResult(self.context, bool())
        qry = ServiceOperationQuery(self, "DisableRecycleBinDiscoverabilityForTenant", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def enable_recycle_bin_discoverability_for_tenant(self) -> ClientResult[bool]:
        """EnableRecycleBinDiscoverabilityForTenant operation."""
        return_type = ClientResult(self.context, bool())
        qry = ServiceOperationQuery(self, "EnableRecycleBinDiscoverabilityForTenant", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def is_recycle_bin_discoverability_enabled_for_tenant(self) -> ClientResult[bool]:
        """IsRecycleBinDiscoverabilityEnabledForTenant operation."""
        return_type = ClientResult(self.context, bool())
        qry = ServiceOperationQuery(self, "IsRecycleBinDiscoverabilityEnabledForTenant", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type
