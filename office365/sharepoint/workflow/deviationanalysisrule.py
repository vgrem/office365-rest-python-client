from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class DeviationAnalysisRule(ClientValue):
    def __init__(
        self,
        definition: Optional[str] = None,
        fallback_clauses: StringCollection = StringCollection(),
        id_: Optional[str] = None,
        is_acceptable: Optional[bool] = None,
        notes: StringCollection = StringCollection(),
        rule_name: Optional[str] = None,
        send_for_approval: Optional[bool] = None,
        snippet_path: Optional[str] = None,
    ):
        self.definition = definition
        self.fallback_clauses = fallback_clauses
        self.id = id_
        self.is_acceptable = is_acceptable
        self.notes = notes
        self.rule_name = rule_name
        self.send_for_approval = send_for_approval
        self.snippet_path = snippet_path
