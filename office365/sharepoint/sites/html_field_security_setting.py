from __future__ import annotations

from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value


@value
class HTMLFieldSecuritySetting(ClientValue):
    allowedDomains: StringCollection = field(default_factory=StringCollection)
    allowEmbedding: Optional[int] = None
