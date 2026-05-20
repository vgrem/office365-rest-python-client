from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class Placeholder(ClientValue):
    data_type: Optional[str] = None
    end_position: Optional[int] = None
    id: Optional[str] = None
    name: Optional[str] = None
    paragraph_id: Optional[str] = None
    question_title: Optional[str] = None
    source: Optional[str] = None
    start_position: Optional[int] = None
