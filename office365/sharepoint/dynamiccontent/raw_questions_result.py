from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.dynamiccontent.question import Question


class RawQuestionsResult(ClientValue):
    Questions: ClientValueCollection[Question] = field(default_factory=lambda: ClientValueCollection(Question))

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.DynamicContent.RawQuestionsResult"
