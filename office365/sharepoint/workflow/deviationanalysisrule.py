from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class DeviationAnalysisRule(ClientValue):
    Definition: str | None = None
    FallbackClauses: StringCollection = field(default_factory=StringCollection)
    Id: UUID | None = None
    IsAcceptable: bool | None = None
    Notes: StringCollection = field(default_factory=StringCollection)
    RuleName: str | None = None
    SendForApproval: bool | None = None
    SnippetPath: str | None = None
