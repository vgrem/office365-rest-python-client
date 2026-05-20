from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class ContentControlInfo(ClientValue):
    content_control_tag_name: Optional[str] = None
    end_index: Optional[int] = None
    is_single_parargaph: Optional[bool] = None
    paragraph_ids: StringCollection = field(default_factory=StringCollection)
    start_index: Optional[int] = None
