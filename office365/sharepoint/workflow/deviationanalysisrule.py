from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class DeviationAnalysisRule(ClientValue):
    definition: Optional[str] = None
    fallback_clauses: StringCollection = field(default_factory=StringCollection)
    id: Optional[str] = None
    is_acceptable: Optional[bool] = None
    notes: StringCollection = field(default_factory=StringCollection)
    rule_name: Optional[str] = None
    send_for_approval: Optional[bool] = None
    snippet_path: Optional[str] = None
