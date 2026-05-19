from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class VersionPolicySelectionParameters(ClientValue):
    file_types_selected: StringCollection = field(default_factory=StringCollection)
    select_all_file_types: bool | None = None
    select_default: bool | None = None
