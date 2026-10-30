from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class UnclassifiedArtifact(Entity):
    @odata(name="kind")
    @property
    def kind(self) -> Optional[str]:
        """Gets the kind property"""
        return self.properties.get("kind", None)

    @odata(name="value")
    @property
    def value(self) -> Optional[str]:
        """Gets the value property"""
        return self.properties.get("value", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.UnclassifiedArtifact"
