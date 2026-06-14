from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import GuidCollection
from office365.sharepoint.dynamiccontent.aggregated_question import AggregatedQuestion


class AggregatedQuestionsPayload(ClientValue):
    AggregatedQuestions: ClientValueCollection[AggregatedQuestion] = field(
        default_factory=lambda: ClientValueCollection(AggregatedQuestion)
    )
    AggregatedRawQuestionIds: GuidCollection = field(default_factory=GuidCollection)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.DynamicContent.AggregatedQuestionsPayload"
