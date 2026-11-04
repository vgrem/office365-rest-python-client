from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ContentAssemblyFormAnswer(ClientValue):
    AdditionalData: str | None = None
    Answer: str | None = None
    ContentControlTagName: str | None = None
