from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ContentAssemblyFormAnswer(ClientValue):
    additional_data: Optional[str] = None
    answer: Optional[str] = None
    content_control_tag_name: Optional[str] = None
