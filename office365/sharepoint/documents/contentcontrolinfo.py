from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value


@value
class ContentControlInfo(ClientValue):
    ContentControlTagName: str | None = None
    EndIndex: int | None = None
    IsSingleParargaph: bool | None = None
    ParagraphIds: StringCollection = field(default_factory=StringCollection)
    StartIndex: int | None = None
