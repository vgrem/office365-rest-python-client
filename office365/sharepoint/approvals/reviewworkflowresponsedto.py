from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ReviewWorkFlowResponseDTO(ClientValue):
    action: Optional[str] = None
    comments: Optional[str] = None
    status: Optional[str] = None
