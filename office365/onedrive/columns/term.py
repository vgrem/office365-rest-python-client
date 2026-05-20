from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TermColumn(ClientValue):
    """Represents a managed metadata column in SharePoint."""

    allowMultipleValues: bool | None = None
    showFullyQualifiedName: bool | None = None
