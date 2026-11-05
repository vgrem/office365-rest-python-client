from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class GetReviewConfigRequestDTO(ClientValue):
    document_uri: Optional[str] = None
