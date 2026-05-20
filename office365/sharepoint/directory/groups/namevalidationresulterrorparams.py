from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class GroupNameValidationResultErrorParams(ClientValue):
    BlockedWord: Optional[str] = None
    Prefix: Optional[str] = None
    Suffix: Optional[str] = None
    ValidationErrorCode: Optional[str] = None
    ValidationErrorMessage: Optional[str] = None
    ValidationPropertyName: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Directory.GroupNameValidationResultErrorParams"
