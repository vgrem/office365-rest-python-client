from __future__ import annotations

from typing import Dict

from typing_extensions import Self

from office365.sharepoint.changes.change import Change
from office365.sharepoint.entity_collection import EntityCollection


class ChangeCollection(EntityCollection[Change]):
    """Represents a collection of Change objects with dynamic type resolution."""

    def __init__(self, context, resource_path=None):
        super().__init__(context, Change, resource_path)

    def set_property(self, key: str, value: Dict, persist_changes: bool = False) -> Self:
        self._resolve_change_type(value)
        super(ChangeCollection, self).set_property(key, value)

    def _resolve_change_type(self, properties: Dict) -> None:
        """Dynamically resolves the appropriate Change type based on properties.

        Args:
            properties: A dictionary of change properties
        """
        from office365.sharepoint.changes.alert import ChangeAlert
        from office365.sharepoint.changes.app_consent_principal import (
            ChangeAppConsentPrincipal,
        )
        from office365.sharepoint.changes.content_type import ChangeContentType
        from office365.sharepoint.changes.field import ChangeField
        from office365.sharepoint.changes.group import ChangeGroup
        from office365.sharepoint.changes.item import ChangeItem
        from office365.sharepoint.changes.list import ChangeList
        from office365.sharepoint.changes.site import ChangeSite
        from office365.sharepoint.changes.user import ChangeUser
        from office365.sharepoint.changes.view import ChangeView
        from office365.sharepoint.changes.web import ChangeWeb

        if not isinstance(properties, dict):
            return

        # Define the resolution mapping
        change_type_mapping = {
            ("ItemId", "ListId"): ChangeItem,
            ("ListId", "WebId"): ChangeList,
            ("WebId",): ChangeWeb,
            ("UserId",): ChangeUser,
            ("GroupId",): ChangeGroup,
            ("ContentTypeId",): ChangeContentType,
            ("AlertId",): ChangeAlert,
            ("FieldId",): ChangeField,
            ("ViewId",): ChangeView,
            ("SiteId",): ChangeSite,
            ("AppConsentPrincipalId",): ChangeAppConsentPrincipal,
        }

        # Find the first matching change type
        for keys, change_type in change_type_mapping.items():
            if all(key in properties for key in keys):
                self._item_type = change_type
                return

        # Default to base Change type if no specific type matches
        self._item_type = Change
