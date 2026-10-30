from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.security.datasecurity.application_mode import ApplicationMode

if TYPE_CHECKING:
    from office365.onedrive.sensitivitylabels.labelactionsource import LabelActionSource
    from office365.security.datasecurity.sensitivity_label import (
        SensitivityLabel,
    )
    from office365.security.datasecurity.usage_rights_included import (
        UsageRightsIncluded,
    )


class SensitivityLabel(Entity):
    """Represents a sensitivity label that defines how to protect and handle content."""

    @odata(name="name")
    @property
    def name(self) -> Optional[str]:
        return self.properties.get("name", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        return self.properties.get("displayName", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        return self.properties.get("description", None)

    @odata(name="priority")
    @property
    def priority(self) -> Optional[int]:
        return self.properties.get("priority", None)

    @property
    def sensitivity(self) -> Optional[int]:
        return self.properties.get("sensitivity", None)

    @property
    def enabled(self) -> Optional[bool]:
        return self.properties.get("enabled", None)

    @odata(name="actionSource")
    @property
    def action_source(self) -> LabelActionSource:
        """Gets the actionSource property"""
        from office365.onedrive.sensitivitylabels.labelactionsource import (
            LabelActionSource,
        )

        return self.properties.get("actionSource", LabelActionSource.manual)

    @odata(name="autoTooltip")
    @property
    def auto_tooltip(self) -> Optional[str]:
        """Gets the autoTooltip property"""
        return self.properties.get("autoTooltip", None)

    @odata(name="hasProtection")
    @property
    def has_protection(self) -> Optional[bool]:
        """Gets the hasProtection property"""
        return self.properties.get("hasProtection", None)

    @odata(name="isDefault")
    @property
    def is_default(self) -> Optional[bool]:
        """Gets the isDefault property"""
        return self.properties.get("isDefault", None)

    @odata(name="isEndpointProtectionEnabled")
    @property
    def is_endpoint_protection_enabled(self) -> Optional[bool]:
        """Gets the isEndpointProtectionEnabled property"""
        return self.properties.get("isEndpointProtectionEnabled", None)

    @odata(name="isScopedToUser")
    @property
    def is_scoped_to_user(self) -> Optional[bool]:
        """Gets the isScopedToUser property"""
        return self.properties.get("isScopedToUser", None)

    @odata(name="locale")
    @property
    def locale(self) -> Optional[str]:
        """Gets the locale property"""
        return self.properties.get("locale", None)

    @odata(name="toolTip")
    @property
    def tool_tip(self) -> Optional[str]:
        """Gets the toolTip property"""
        return self.properties.get("toolTip", None)

    @odata(name="rights", navigation=True)
    @property
    def rights(self) -> UsageRightsIncluded:
        """Gets the rights property"""
        from office365.security.datasecurity.usage_rights_included import (
            UsageRightsIncluded,
        )

        return self.properties.get(
            "rights", UsageRightsIncluded(self.context, ResourcePath("rights", self.resource_path))
        )

    @odata(name="sublabels", navigation=True)
    @property
    def sublabels(self) -> EntityCollection[SensitivityLabel]:
        """Gets the sublabels property"""
        from office365.security.datasecurity.sensitivity_label import (
            SensitivityLabel,
        )

        return self.properties.get(
            "sublabels",
            EntityCollection[SensitivityLabel](
                self.context, SensitivityLabel, ResourcePath("sublabels", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SensitivityLabel"

    @odata(name="applicationMode")
    @property
    def application_mode(self) -> Optional[ApplicationMode]:
        """Gets the applicationMode property"""
        return self.properties.get("applicationMode", None)
