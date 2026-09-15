from __future__ import annotations

from uuid import UUID

from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity
from office365.sharepoint.tenant.administration.catalog_management_custom_property_map import (
    CatalogManagementCustomPropertyMap,
)
from office365.sharepoint.tenant.administration.custom_site_property_data import CustomSitePropertyData
from office365.sharepoint.tenant.administration.extended_attribute_settings import ExtendedAttributeSettings
from office365.sharepoint.tenant.administration.uploaded_site_category import UploadedSiteCategory
from office365.sharepoint.tenant.administration.uploaded_site_category_metadata import UploadedSiteCategoryMetadata
from office365.sharepoint.tenant.administration.uploaded_site_group_definition import UploadedSiteGroupDefinition


class CatalogManagementCustomPropertiesCollection(Entity):
    def add_site_property_bag_mappings(
        self, property_bag_keys: list[str]
    ) -> ClientResult[CatalogManagementCustomPropertyMap]:
        """AddSitePropertyBagMappings operation.

        Args:
            property_bag_keys (list[str]): propertyBagKeys parameter
        """
        return_type = ClientResult(self.context, CatalogManagementCustomPropertyMap())
        qry = ServiceOperationQuery(
            self,
            "AddSitePropertyBagMappings",
            None,
            {"propertyBagKeys": StringCollection(property_bag_keys)},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def export_category_group_to_csv(self, source: int, key: str, value_id: UUID, group_name: str) -> ClientResult[str]:
        """ExportCategoryGroupToCSV operation.

        Args:
            source (int): source parameter
            key (str): key parameter
            value_id (UUID): valueId parameter
            group_name (str): groupName parameter
        """
        return_type = ClientResult(self.context, str())
        qry = ServiceOperationQuery(
            self,
            "ExportCategoryGroupToCSV",
            None,
            {"source": source, "key": key, "valueId": value_id, "groupName": group_name},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def export_category_to_csv(self, source: int, key: str, value_id: UUID) -> ClientResult[str]:
        """ExportCategoryToCSV operation.

        Args:
            source (int): source parameter
            key (str): key parameter
            value_id (UUID): valueId parameter
        """
        return_type = ClientResult(self.context, str())
        qry = FunctionQuery(self, "ExportCategoryToCSV", [source, key, value_id], return_type)
        self.context.add_query(qry)
        return return_type

    def export_category_to_csv_by_group(
        self, source: int, key: str, value_id: UUID, group_name: str
    ) -> ClientResult[str]:
        """ExportCategoryToCSVByGroup operation.

        Args:
            source (int): source parameter
            key (str): key parameter
            value_id (UUID): valueId parameter
            group_name (str): groupName parameter
        """
        return_type = ClientResult(self.context, str())
        qry = FunctionQuery(self, "ExportCategoryToCSVByGroup", [source, key, value_id, group_name], return_type)
        self.context.add_query(qry)
        return return_type

    def get_custom_property_map(self) -> ClientResult[CatalogManagementCustomPropertyMap]:
        """GetCustomPropertyMap operation."""
        return_type = ClientResult(self.context, CatalogManagementCustomPropertyMap())
        qry = FunctionQuery(self, "GetCustomPropertyMap", [], return_type)
        self.context.add_query(qry)
        return return_type

    def get_custom_site_property_data(self) -> ClientResult[ClientValueCollection[CustomSitePropertyData]]:
        """GetCustomSitePropertyData operation."""
        return_type = ClientResult(self.context, ClientValueCollection[CustomSitePropertyData]())
        qry = FunctionQuery(self, "GetCustomSitePropertyData", [], return_type)
        self.context.add_query(qry)
        return return_type

    def get_extended_attribute_settings(self) -> ClientResult[ClientValueCollection[ExtendedAttributeSettings]]:
        """GetExtendedAttributeSettings operation."""
        return_type = ClientResult(self.context, ClientValueCollection[ExtendedAttributeSettings]())
        qry = FunctionQuery(self, "GetExtendedAttributeSettings", [], return_type)
        self.context.add_query(qry)
        return return_type

    def get_site_property_bag_site_list(self) -> ClientResult[StringCollection]:
        """GetSitePropertyBagSiteList operation."""
        return_type = ClientResult(self.context, StringCollection())
        qry = FunctionQuery(self, "GetSitePropertyBagSiteList", [], return_type)
        self.context.add_query(qry)
        return return_type

    def get_uploaded_site_categories(self) -> ClientResult[ClientValueCollection[UploadedSiteCategoryMetadata]]:
        """GetUploadedSiteCategories operation."""
        return_type = ClientResult(self.context, ClientValueCollection[UploadedSiteCategoryMetadata]())
        qry = FunctionQuery(self, "GetUploadedSiteCategories", [], return_type)
        self.context.add_query(qry)
        return return_type

    def get_uploaded_site_category_detail(
        self, category_id: str
    ) -> ClientResult[ClientValueCollection[UploadedSiteGroupDefinition]]:
        """GetUploadedSiteCategoryDetail operation.

        Args:
            category_id (str): categoryId parameter
        """
        return_type = ClientResult(self.context, ClientValueCollection[UploadedSiteGroupDefinition]())
        qry = FunctionQuery(self, "GetUploadedSiteCategoryDetail", [category_id], return_type)
        self.context.add_query(qry)
        return return_type

    def remove_site_property_bag_mapping(
        self, site_property_key: str
    ) -> ClientResult[CatalogManagementCustomPropertyMap]:
        """RemoveSitePropertyBagMapping operation.

        Args:
            site_property_key (str): sitePropertyKey parameter
        """
        return_type = ClientResult(self.context, CatalogManagementCustomPropertyMap())
        qry = ServiceOperationQuery(
            self, "RemoveSitePropertyBagMapping", None, {"sitePropertyKey": site_property_key}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def remove_uploaded_site_category(
        self, category_id: str
    ) -> ClientResult[ClientValueCollection[UploadedSiteCategoryMetadata]]:
        """RemoveUploadedSiteCategory operation.

        Args:
            category_id (str): categoryId parameter
        """
        return_type = ClientResult(self.context, ClientValueCollection[UploadedSiteCategoryMetadata]())
        qry = ServiceOperationQuery(
            self, "RemoveUploadedSiteCategory", None, {"categoryId": category_id}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def set_extended_attribute_settings(
        self, extended_attributes: ClientValueCollection[ExtendedAttributeSettings]
    ) -> ClientResult[ClientValueCollection[ExtendedAttributeSettings]]:
        """SetExtendedAttributeSettings operation.

        Args:
            extended_attributes (ClientValueCollection[ExtendedAttributeSettings]): extendedAttributes parameter
        """
        return_type = ClientResult(self.context, ClientValueCollection[ExtendedAttributeSettings]())
        qry = ServiceOperationQuery(
            self, "SetExtendedAttributeSettings", None, {"extendedAttributes": extended_attributes}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def set_site_property_bag_config(
        self, site_property_mapping: dict
    ) -> ClientResult[CatalogManagementCustomPropertyMap]:
        """SetSitePropertyBagConfig operation.

        Args:
            site_property_mapping (dict): sitePropertyMapping parameter
        """
        return_type = ClientResult(self.context, CatalogManagementCustomPropertyMap())
        qry = ServiceOperationQuery(
            self, "SetSitePropertyBagConfig", None, {"sitePropertyMapping": site_property_mapping}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def set_site_property_bag_scope_config(
        self, sites_option: int, site_urls: list[str], uploaded_file_name: str
    ) -> ClientResult[CatalogManagementCustomPropertyMap]:
        """SetSitePropertyBagScopeConfig operation.

        Args:
            sites_option (int): sitesOption parameter
            site_urls (list[str]): siteUrls parameter
            uploaded_file_name (str): uploadedFileName parameter
        """
        return_type = ClientResult(self.context, CatalogManagementCustomPropertyMap())
        qry = ServiceOperationQuery(
            self,
            "SetSitePropertyBagScopeConfig",
            None,
            {
                "sitesOption": sites_option,
                "siteUrls": StringCollection(site_urls),
                "uploadedFileName": uploaded_file_name,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def set_uploaded_site_category(
        self, category: UploadedSiteCategory
    ) -> ClientResult[ClientValueCollection[UploadedSiteCategoryMetadata]]:
        """SetUploadedSiteCategory operation.

        Args:
            category (UploadedSiteCategory): category parameter
        """
        return_type = ClientResult(self.context, ClientValueCollection[UploadedSiteCategoryMetadata]())
        qry = ServiceOperationQuery(self, "SetUploadedSiteCategory", None, {"category": category}, None, return_type)
        self.context.add_query(qry)
        return return_type
