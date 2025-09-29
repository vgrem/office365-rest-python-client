from typing import Optional

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.v3.static import StaticPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class TenantSettings(Entity):
    """Specifies the tenant properties."""

    def clear_corporate_catalog(self) -> Self:
        """"""
        qry = ServiceOperationQuery(
            self, "ClearCorporateCatalog", None, None, None, None
        )
        self.context.add_query(qry)
        return self

    def get_data_access_governance_report_config(self) -> ClientResult[str]:
        """ """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self, "GetDataAccessGovernanceReportConfig", None, None, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def set_corporate_catalog(self, url: str) -> Self:
        """
        :param str url:
        """
        payload = {"url": url}
        qry = ServiceOperationQuery(
            self, "SetCorporateCatalog", None, payload, None, None
        )
        self.context.add_query(qry)
        return self

    @property
    def corporate_catalog_url(self) -> Optional[str]:
        """Specifies the URL of the corporate catalog site collection."""
        return self.properties.get("CorporateCatalogUrl", None)

    @staticmethod
    def current(context):
        """
        Specifies the current instance for the SP.TenantSettings.
        :type context: office365.sharepoint.client_context.ClientContext
        """
        return TenantSettings(context, StaticPath("SP.TenantSettings.Current"))
