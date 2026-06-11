from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class CAAESnippetElement(ClientValue):
    Id: str | None = None
    Version: str | None = None
