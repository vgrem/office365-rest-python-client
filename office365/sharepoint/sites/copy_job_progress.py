from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class CopyJobProgress(ClientValue):
    JobState: int | None = None
    Logs: StringCollection = field(default_factory=StringCollection)
