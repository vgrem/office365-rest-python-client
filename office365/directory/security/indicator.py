from __future__ import annotations

from office365.directory.security.artifact import Artifact
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath


class Indicator(Entity):
    @property
    def artifact(self) -> Artifact:
        """Gets the artifact property"""
        return self.properties.get("artifact", Artifact(self.context, ResourcePath("artifact", self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.Indicator"
