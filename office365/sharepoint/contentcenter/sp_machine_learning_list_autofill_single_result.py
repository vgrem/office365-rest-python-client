from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SPMachineLearningListAutofillSingleResult(ClientValue):
    ItemId: int | None = None
    Status: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Office.Server.ContentCenter.SPMachineLearningListAutofillSingleResult"
