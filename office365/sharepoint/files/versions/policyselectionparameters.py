from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class VersionPolicySelectionParameters(ClientValue):
    FileTypesSelected: StringCollection = field(default_factory=StringCollection)
    SelectAllFileTypes: bool | None = None
    SelectDefault: bool | None = None
