from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPMachineLearningListAutofillEntityData(ClientValue):
    FillMode: str | None = None
    ListId: UUID | None = None
    TargetItemIds: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Office.Server.ContentCenter.SPMachineLearningListAutofillEntityData"
