from __future__ import annotations

from office365.directory.authentication.featuretargettype import FeatureTargetType
from office365.runtime.client_value import ClientValue


class FeatureTarget(ClientValue):
    def __init__(
        self,
        id_: str | None = None,
        target_type: FeatureTargetType = FeatureTargetType.none,
    ):
        self.id = id_
        self.targetType = target_type

    @property
    def entity_type_name(self):
        return "microsoft.graph.FeatureTarget"
