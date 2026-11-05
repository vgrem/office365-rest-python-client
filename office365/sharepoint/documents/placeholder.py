from __future__ import annotations

from office365.runtime.client_value import ClientValue


class Placeholder(ClientValue):
    DataType: str | None = None
    EndPosition: int | None = None
    Id: str | None = None
    Name: str | None = None
    ParagraphId: str | None = None
    QuestionTitle: str | None = None
    Source: str | None = None
    StartPosition: int | None = None
