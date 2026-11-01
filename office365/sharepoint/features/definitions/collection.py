from __future__ import annotations

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.features.definitions.definition import FeatureDefinition
from office365.sharepoint.permissions import SiteLevel, site_access


class FeatureDefinitionCollection(EntityCollection[FeatureDefinition]):
    """Represents a collection of feature's definitions"""

    def __init__(self, context, resource_path=None, parent=None):
        super().__init__(context, FeatureDefinition, resource_path, parent)

    @site_access(SiteLevel.READ)
    def get_feature_definition(
        self,
        feature_display_name: str,
        compatibility_level: int | None = None,
    ) -> FeatureDefinition:
        """Retrieves a feature definition by display name.

        Args:
            feature_display_name: The display name of the feature definition.
            compatibility_level: Optional compatibility level filter.
        """
        return_type = FeatureDefinition(self.context)
        payload = {
            "featureDisplayName": feature_display_name,
            "compatibilityLevel": compatibility_level,
        }
        qry = ServiceOperationQuery(self, "GetFeatureDefinition", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type
