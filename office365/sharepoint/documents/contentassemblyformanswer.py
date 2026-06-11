from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ContentAssemblyFormAnswer(ClientValue):
    AdditionalData: str | None = None
    Answer: str | None = None
    ContentControlTagName: str | None = None
