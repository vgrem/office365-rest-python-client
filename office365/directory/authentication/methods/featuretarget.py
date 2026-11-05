from __future__ import annotations

from office365.directory.authentication.featuretargettype import FeatureTargetType
from office365.runtime.client_value import ClientValue


class FeatureTarget(ClientValue):
    id: str | None = None
    targetType: FeatureTargetType = FeatureTargetType.none

    @property
    def entity_type_name(self):
        return "microsoft.graph.FeatureTarget"
