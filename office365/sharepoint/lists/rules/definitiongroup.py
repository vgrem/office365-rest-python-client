from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.lists.rules.definition import RulesDefinition


class RulesDefinitionGroup(ClientValue):
    def __init__(
        self,
        rule_definitions_list: ClientValueCollection[RulesDefinition] = ClientValueCollection(RulesDefinition),
        rule_group: str = None,
    ):
        self.rule_definitions_list = rule_definitions_list
        self.rule_group = rule_group
