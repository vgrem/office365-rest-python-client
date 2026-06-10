from __future__ import annotations

from typing import Any

from office365.entity_collection import EntityCollection
from office365.outlook.categories.category import OutlookCategory


class OutlookCategoryCollection(EntityCollection[OutlookCategory]):
    def __init__(self, context, resource_path=None):
        super().__init__(context, OutlookCategory, resource_path)

    def add(self, display_name: str, color: str | None, **kwargs: Any) -> OutlookCategory:
        """Create a new category object.

        Args:
            display_name (str): Display name of the application.
            color (str): Color of the category.
        """
        props = {
            "displayName": display_name,
            "color": color,
            **kwargs,
        }
        return super().add(**props)
