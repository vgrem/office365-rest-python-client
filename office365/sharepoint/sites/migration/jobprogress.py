from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class MigrationJobProgress(ClientValue):
    logs: StringCollection = field(default_factory=StringCollection)
    next_token: Optional[str] = None
