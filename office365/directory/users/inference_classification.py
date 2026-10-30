from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.users.inference_classification_override import (
        InferenceClassificationOverride,
    )


class InferenceClassification(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.InferenceClassification"

    @odata(name="overrides", navigation=True)
    @property
    def overrides(self) -> EntityCollection[InferenceClassificationOverride]:
        """Gets the overrides property"""
        from office365.directory.users.inference_classification_override import (
            InferenceClassificationOverride,
        )

        return self.properties.get(
            "overrides",
            EntityCollection[InferenceClassificationOverride](
                self.context, InferenceClassificationOverride, ResourcePath("overrides", self.resource_path)
            ),
        )
