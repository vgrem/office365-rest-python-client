from __future__ import annotations

from dataclasses import dataclass

from office365.onedrive.termstore.sets.set import Set
from office365.onedrive.termstore.terms.term import Term
from office365.runtime.client_value import ClientValue


@dataclass
class TermColumn(ClientValue):
    """Represents a managed metadata column in SharePoint."""

    allowMultipleValues: bool | None = None
    showFullyQualifiedName: bool | None = None
    parentTerm: Term | None = None
    termSet: Set | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TermColumn"
