from __future__ import annotations

from dataclasses import field
from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


class Question(ClientValue):
    CreatedTime: datetime | None = field(default_factory=lambda: datetime.min)
    Id: UUID | None = None
    QuestionText: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.DynamicContent.Question"
