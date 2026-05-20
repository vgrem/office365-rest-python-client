from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ConfiguredMetadataNavigationItem(ClientValue):
    """Represents a configured metadata navigation item.

    field_display_name: The display name of the field that this item refers to.
    field_title: The internal name of the field that this item refers to.
    field_type_as_string: The type of the field that this item refers to.
    is_content_type_field: Indicates whether the type of this field is a content type.
    is_folder_hierarchy: Indicates whether this item is a folder hierarchy.
    is_hierarchy: Indicates whether this item is hierarchical.
    """

    FieldDisplayName: Optional[str] = None
    FieldTitle: Optional[str] = None
    FieldTypeAsString: Optional[str] = None
    IsContentTypeField: Optional[bool] = None
    IsFolderHierarchy: Optional[bool] = None
    IsHierarchy: Optional[bool] = None
    IsMultiValueLookup: Optional[bool] = None
    IsTaxonomyField: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.MetadataNavigation.ConfiguredMetadataNavigationItem"
