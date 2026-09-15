from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.function import FunctionQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.publishing.propertyvalue import PropertyValue
from office365.sharepoint.tenant.administration.property import Property


class CatalogManagementCollection(Entity):
    @property
    def last_updated_time_utc(self) -> Optional[datetime]:
        """Gets the lastUpdatedTimeUtc property"""
        return self.properties.get("lastUpdatedTimeUtc", datetime.min)

    @property
    def items(self) -> ClientValueCollection[Property]:
        """Gets the Items property"""
        return self.properties.get("Items", ClientValueCollection[Property](Property))

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.CatalogManagementCollection"

    def export_property_type_to_csv(self, property_type: int) -> ClientResult[str]:
        """ExportPropertyTypeToCSV operation.

        Args:
            property_type (int): propertyType parameter
        """
        return_type = ClientResult(self.context, str())
        qry = FunctionQuery(self, "ExportPropertyTypeToCSV", [property_type], return_type)
        self.context.add_query(qry)
        return return_type

    def export_to_csv(self, property_type: int, value_id: UUID) -> ClientResult[str]:
        """ExportToCSV operation.

        Args:
            property_type (int): propertyType parameter
            value_id (UUID): valueId parameter
        """
        return_type = ClientResult(self.context, str())
        qry = FunctionQuery(self, "ExportToCSV", [property_type, value_id], return_type)
        self.context.add_query(qry)
        return return_type

    def get_display_names(self) -> ClientResult[dict]:
        """GetDisplayNames operation."""
        return_type = ClientResult(self.context, dict())
        qry = FunctionQuery(self, "GetDisplayNames", [], return_type)
        self.context.add_query(qry)
        return return_type

    def get_value(self, property_id: UUID) -> ClientResult[PropertyValue]:
        """GetValue operation.

        Args:
            property_id (UUID): propertyId parameter
        """
        return_type = ClientResult(self.context, PropertyValue())
        qry = FunctionQuery(self, "GetValue", [property_id], return_type)
        self.context.add_query(qry)
        return return_type
