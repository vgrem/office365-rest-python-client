from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class PivotItem(ClientValue):
    audiences: StringCollection = field(default_factory=StringCollection)
    name: Optional[str] = None
