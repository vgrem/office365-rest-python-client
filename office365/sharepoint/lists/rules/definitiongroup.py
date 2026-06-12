from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.lists.rules.definition import RulesDefinition


@dataclass
class RulesDefinitionGroup(ClientValue):
    RuleDefinitionsList: ClientValueCollection[RulesDefinition] = field(
        default_factory=lambda: ClientValueCollection(RulesDefinition)
    )
    RuleGroup: str | None = None
