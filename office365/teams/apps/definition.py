from __future__ import annotations

from datetime import datetime

from office365.directory.permissions.identity_set import IdentitySet
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.teams.bots.teamwork_bot import TeamworkBot


class TeamsAppDefinition(Entity):
    """Represents the details of a version of a teamsApp."""

    @property
    def bot(self) -> TeamworkBot:
        """The details of the bot specified in the Teams app manifest."""
        return self.properties.get("bot", TeamworkBot(self.context, ResourcePath("bot", self.resource_path)))

    @odata(name="createdBy")
    @property
    def created_by(self) -> IdentitySet:
        """Identity of the user, device, or application which created the item."""
        return self.properties.get("createdBy", IdentitySet())

    @property
    def description(self) -> str | None:
        """Verbose description of the application."""
        return self.properties.get("description", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_datetime(self) -> datetime:
        """Gets date and time the teamsApp was last modified."""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @property
    def teams_app_id(self) -> str | None:
        """The ID from the Teams app manifest."""
        return self.properties.get("teamsAppId", None)
