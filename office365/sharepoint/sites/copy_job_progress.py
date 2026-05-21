from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class CopyJobProgress(ClientValue):
    JobState: str | None = None
    Logs: StringCollection = field(default_factory=StringCollection)
