from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.v4.entity import EntityPath


class JoinedTeamsPath(EntityPath):
    def __init__(self, parent, collection=None):
        super().__init__("joinedTeams", parent, ResourcePath("teams"))
