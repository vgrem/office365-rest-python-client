from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class MigrationJobProgress(ClientValue):
    Logs: StringCollection = field(default_factory=StringCollection)
    NextToken: str | None = None
