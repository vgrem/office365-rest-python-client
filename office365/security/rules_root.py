from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.security.detection_rule import DetectionRule


class RulesRoot(Entity):
    @odata(name="detectionRules", navigation=True)
    @property
    def detection_rules(self) -> EntityCollection[DetectionRule]:
        """Gets the detectionRules property"""
        from office365.security.detection_rule import DetectionRule

        return self.properties.get(
            "detectionRules",
            EntityCollection[DetectionRule](
                self.context, DetectionRule, ResourcePath("detectionRules", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.RulesRoot"
