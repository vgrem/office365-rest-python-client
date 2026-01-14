from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class DeviationAnalysisRule(ClientValue):
    def __init__(
        self,
        definition: str = None,
        fallback_clauses: StringCollection = StringCollection(),
        id_: str = None,
        is_acceptable: bool = None,
        notes: StringCollection = StringCollection(),
        rule_name: str = None,
        send_for_approval: bool = None,
        snippet_path: str = None,
    ):
        self.definition = definition
        self.fallback_clauses = fallback_clauses
        self.id = id_
        self.is_acceptable = is_acceptable
        self.notes = notes
        self.rule_name = rule_name
        self.send_for_approval = send_for_approval
        self.snippet_path = snippet_path
