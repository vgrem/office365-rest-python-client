from __future__ import annotations

from dataclasses import field
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.sharepoint.contentcenter.machinelearning.column_autofill_choice_settings import (
    SPMachineLearningColumnAutofillChoiceSettings,
)


class SPMachineLearningColumnAutofillPreviewData(ClientValue):
    ChoiceSettings: SPMachineLearningColumnAutofillChoiceSettings = field(
        default_factory=SPMachineLearningColumnAutofillChoiceSettings
    )
    ColumnDataType: str | None = None
    ColumnInternalName: str | None = None
    DisplayName: str | None = None
    ItemId: int | None = None
    ListId: UUID | None = None
    Prompt: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Office.Server.ContentCenter.SPMachineLearningColumnAutofillPreviewData"
