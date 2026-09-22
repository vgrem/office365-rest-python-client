from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.limits import Limit


@dataclass
class AssessmentIssue:
    severity: str  # blocker | warning | info
    category: str  # path | field | permission | file | workflow
    location: str  # list/folder/field path
    message: str
    suggestion: str = ""
    risk_code: str = ""  # product-specific scan-assessment code (SPMT), when applicable
    limit: Optional[Limit] = None  # the authoritative (product-agnostic) limit, when applicable


#: SPMT scan-assessment risk codes the library can emit (a subset — the ones tied
#: to SharePoint service limits). See
#: https://learn.microsoft.com/en-us/sharepointmigration/spmt-scan-risk-codes
RISK_CODES: dict[str, str] = {
    "LIST_VIEW_EXCEED_LIMIT": "The list view shows more items than the list view threshold.",
    "ITEM_COUNT_EXCEED_INDEX_LIMIT": "Item count is too large to create a column index.",
    "ITEM_COUNT_EXCEED_LIMIT": "Item count exceeds the per-list maximum.",
    "LIST_VIEW_LOOKUP_EXCEED_LIMIT": "Lookup/people/managed-metadata columns exceed the list view lookup threshold.",
    "UNIQUE_PERMISSION_EXCEED_LIMIT": "Unique permissions per list exceed the supported/recommended limit.",
}
