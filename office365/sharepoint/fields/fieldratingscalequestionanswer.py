from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class FieldRatingScaleQuestionAnswer(ClientValue):
    answer: int | None = None
    question: str | None = None
