from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata
from office365.security.threatintelligence.host_reputation_classification import HostReputationClassification

if TYPE_CHECKING:
    from office365.security.threatintelligence.host_reputation_rule import (
        HostReputationRule,
    )


class HostReputation(Entity):
    @odata(name="score")
    @property
    def score(self) -> Optional[int]:
        """Gets the score property"""
        return self.properties.get("score", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.HostReputation"

    @odata(name="classification")
    @property
    def classification(self) -> HostReputationClassification:
        """Gets the classification property"""
        return self.properties.get("classification", HostReputationClassification.unknown)

    @odata(name="rules")
    @property
    def rules(self) -> ClientValueCollection[HostReputationRule]:
        """Gets the rules property"""
        from office365.security.threatintelligence.host_reputation_rule import (
            HostReputationRule,
        )

        return self.properties.get("rules", ClientValueCollection[HostReputationRule](HostReputationRule))
