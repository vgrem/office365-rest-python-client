from __future__ import annotations

from dataclasses import dataclass

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

    FieldDisplayName: str | None = None
    FieldTitle: str | None = None
    FieldTypeAsString: str | None = None
    IsContentTypeField: bool | None = None
    IsFolderHierarchy: bool | None = None
    IsHierarchy: bool | None = None
    IsMultiValueLookup: bool | None = None
    IsTaxonomyField: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "SP.MetadataNavigation.ConfiguredMetadataNavigationItem"
