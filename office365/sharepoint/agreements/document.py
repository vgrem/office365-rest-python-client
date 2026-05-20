from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class AgreementDocument(ClientValue):
    DocumentType: Optional[str] = None
    DocumentUrl: Optional[str] = None
    IsActive: Optional[bool] = None
    LinkedPDFs: StringCollection = field(default_factory=StringCollection)
    State: Optional[str] = None
