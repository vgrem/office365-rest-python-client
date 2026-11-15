from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version
from office365.teams.apps.dashboard_card_content_source import TeamsAppDashboardCardContentSource
from office365.teams.apps.dashboard_card_icon import TeamsAppDashboardCardIcon
from office365.teams.apps.dashboard_card_size import TeamsAppDashboardCardSize


@version("beta")
class TeamsAppDashboardCardDefinition(Entity):
    @odata(name="contentSource")
    @property
    def content_source(self) -> Optional[TeamsAppDashboardCardContentSource]:
        """Gets the contentSource property"""
        return self.properties.get("contentSource", None)

    @odata(name="defaultSize")
    @property
    def default_size(self) -> Optional[TeamsAppDashboardCardSize]:
        """Gets the defaultSize property"""
        return self.properties.get("defaultSize", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="icon")
    @property
    def icon(self) -> Optional[TeamsAppDashboardCardIcon]:
        """Gets the icon property"""
        return self.properties.get("icon", None)

    @odata(name="pickerGroupId")
    @property
    def picker_group_id(self) -> Optional[str]:
        """Gets the pickerGroupId property"""
        return self.properties.get("pickerGroupId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamsAppDashboardCardDefinition"
