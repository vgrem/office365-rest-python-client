from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ReviewWorkFlowResponseDTO(ClientValue):
    action: Optional[str] = None
    comments: Optional[str] = None
    status: Optional[str] = None
