from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.lists.rules.definition import RulesDefinition


class RulesDefinitionGroup(ClientValue):
    RuleDefinitionsList: ClientValueCollection[RulesDefinition] = field(
        default_factory=lambda: ClientValueCollection(RulesDefinition)
    )
    RuleGroup: str | None = None
