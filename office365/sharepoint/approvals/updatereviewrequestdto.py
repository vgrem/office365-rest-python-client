from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class UpdateReviewRequestDTO(ClientValue):
    action: Optional[str] = None
    comments: Optional[str] = None
    document_uri: Optional[str] = None
    reviewer_email_or_upn: Optional[str] = None
