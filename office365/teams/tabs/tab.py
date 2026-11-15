from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.teams.apps.app import TeamsApp
from office365.teams.tabs.configuration import TeamsTabConfiguration


class TeamsTab(Entity):
    """
    A teamsTab is a tab that's pinned (attached) to a channel within a team.
    """

    @odata(name="teamsApp", navigation=True)
    @property
    def teams_app(self) -> TeamsApp:
        """The application that is linked to the tab. This cannot be changed after tab creation."""
        return self.properties.get(
            "teamsApp",
            TeamsApp(self.context, ResourcePath("teamsApp", self.resource_path)),
        )

    @odata(name="configuration")
    @property
    def configuration(self) -> TeamsTabConfiguration:
        """
        Container for custom settings applied to a tab. The tab is considered configured only once this property is set.
        """
        return self.properties.get("configuration", TeamsTabConfiguration())

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="webUrl")
    @property
    def web_url(self) -> Optional[str]:
        """Gets the webUrl property"""
        return self.properties.get("webUrl", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamsTab"

    @odata(name="messageId", beta=True)
    @property
    def message_id(self) -> Optional[str]:
        """Gets the messageId property"""
        return self.properties.get("messageId", None)

    @odata(name="sortOrderIndex", beta=True)
    @property
    def sort_order_index(self) -> Optional[str]:
        """Gets the sortOrderIndex property"""
        return self.properties.get("sortOrderIndex", None)

    @odata(name="teamsAppId", beta=True)
    @property
    def teams_app_id(self) -> Optional[str]:
        """Gets the teamsAppId property"""
        return self.properties.get("teamsAppId", None)
