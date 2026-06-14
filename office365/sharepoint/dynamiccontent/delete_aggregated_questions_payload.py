from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


class DeleteAggregatedQuestionsPayload(ClientValue):
    QuestionIds: GuidCollection = field(default_factory=GuidCollection)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.DynamicContent.DeleteAggregatedQuestionsPayload"
