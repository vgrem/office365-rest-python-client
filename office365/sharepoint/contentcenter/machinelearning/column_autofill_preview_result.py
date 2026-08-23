from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SPMachineLearningColumnAutofillPreviewResult(ClientValue):
    Status: str | None = None
    Value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Office.Server.ContentCenter.SPMachineLearningColumnAutofillPreviewResult"
