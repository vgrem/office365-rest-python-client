from __future__ import annotations

from uuid import UUID

from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.tenant.administration.rcd_categories_map import RcdCategoriesMap
from office365.sharepoint.tenant.administration.rcd_category_detail_result import RcdCategoryDetailResult
from office365.sharepoint.tenant.administration.rcd_group_definition import RcdGroupDefinition
from office365.sharepoint.tenant.administration.rcd_save_result import RcdSaveResult


class CatalogManagementRestrictedContentDiscoveryCollection(Entity):
    def export_rcd_sites_to_csv(self, group_id: UUID, status_filter: str) -> ClientResult[str]:
        """ExportRcdSitesToCsv operation.

        Args:
            group_id (UUID): groupId parameter
            status_filter (str): statusFilter parameter
        """
        return_type = ClientResult(self.context, str())
        qry = FunctionQuery(self, "ExportRcdSitesToCsv", [group_id, status_filter], return_type)
        self.context.add_query(qry)
        return return_type

    def get_rcd_categories(self) -> ClientResult[RcdCategoriesMap]:
        """GetRcdCategories operation."""
        return_type = ClientResult(self.context, RcdCategoriesMap())
        qry = FunctionQuery(self, "GetRcdCategories", [], return_type)
        self.context.add_query(qry)
        return return_type

    def get_rcd_group_detail(self, group_id: UUID) -> ClientResult[RcdCategoryDetailResult]:
        """GetRcdGroupDetail operation.

        Args:
            group_id (UUID): groupId parameter
        """
        return_type = ClientResult(self.context, RcdCategoryDetailResult())
        qry = FunctionQuery(self, "GetRcdGroupDetail", [group_id], return_type)
        self.context.add_query(qry)
        return return_type

    def save_rcd_categories(self, categories: ClientValueCollection[RcdGroupDefinition]) -> ClientResult[RcdSaveResult]:
        """SaveRcdCategories operation.

        Args:
            categories (ClientValueCollection[RcdGroupDefinition]): categories parameter
        """
        return_type = ClientResult(self.context, RcdSaveResult())
        qry = ServiceOperationQuery(self, "SaveRcdCategories", None, {"categories": categories}, None, return_type)
        self.context.add_query(qry)
        return return_type
