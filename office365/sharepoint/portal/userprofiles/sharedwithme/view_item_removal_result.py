from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SharedWithMeViewItemRemovalResult(ClientValue):
    """An object that contains the result of calling the API to remove an item from a user's 'Shared With Me' view."""

    ErrorCode: Optional[int] = None
    ErrorMessage: Optional[str] = None
    Success: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharedWithMeViewItemRemovalResult"
