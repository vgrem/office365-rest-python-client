from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ContentApprovalStatusColumn(ClientValue):
    """Represents a content approval status column in SharePoint."""
