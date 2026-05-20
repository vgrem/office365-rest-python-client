from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.lists.rules.definition import RulesDefinition


@dataclass
class RulesDefinitionGroup(ClientValue):
    rule_definitions_list: ClientValueCollection[RulesDefinition] = field(
        default_factory=lambda: ClientValueCollection(RulesDefinition)
    )
    rule_group: Optional[str] = None
