from typing import Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.teams.teamwork.tags.member import TeamworkTagMember
from office365.teams.teamwork.tagtype import TeamworkTagType


class TeamworkTag(Entity):
    """
    Represents a tag associated with a team.

    Tags provide a flexible way for customers to classify users or groups based on a auth attribute within a team.
    For example, a Nurse, Manager, or Designer tag will enable users to reach groups of people in Teams without
    having to type every single name.

    When a tag is added, users can @mention it in a channel. Everyone who has been assigned that tag will receive
    a notification just as they would if they were @mentioned individually. Users can also use a tag to start
    a new chat with the members of that tag.
    """

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """The description of the tag as it appears to users in Teams."""
        return self.properties.get("description", None)

    @property
    def display_name(self) -> Optional[str]:
        """The name of the tag as it appears to users in Teams."""
        return self.properties.get("displayName", None)

    @odata(name="memberCount")
    @property
    def member_count(self) -> Optional[int]:
        """The number of users assigned to the tag."""
        return self.properties.get("memberCount", None)

    @odata(name="tagType")
    @property
    def tag_type(self) -> Optional[TeamworkTagType]:
        """The type of the tag (standard or unknownFutureValue)."""
        return self.properties.get("tagType", None)

    @odata(name="teamId")
    @property
    def team_id(self) -> Optional[str]:
        """The ID of the team to which the tag belongs."""
        return self.properties.get("teamId", None)

    @property
    def members(self) -> EntityCollection[TeamworkTagMember]:
        """The members assigned to the tag."""
        return self.properties.get(
            "members",
            EntityCollection(self.context, TeamworkTagMember, ResourcePath("members", self.resource_path)),
        )
