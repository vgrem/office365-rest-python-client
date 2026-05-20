from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class UpdateReviewRequestDTO(ClientValue):
    action: Optional[str] = None
    comments: Optional[str] = None
    document_uri: Optional[str] = None
    reviewer_email_or_upn: Optional[str] = None
