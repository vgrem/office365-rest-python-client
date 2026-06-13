from __future__ import annotations

from dataclasses import field
from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


class SerilizableMoveJobEntityData(ClientValue):
    ApiVersion: str | None = None
    BatchId: UUID | None = None
    CancelTriggeredBy: str | None = None
    DestinationDataLocation: str | None = None
    Direction: int | None = None
    ErrorMessage: str | None = None
    FinishedDateInUtc: datetime | None = field(default_factory=lambda: datetime.min)
    Id: UUID | None = None
    IsReadOnlyAlertRaised: bool | None = None
    JobPhase: int | None = None
    Notify: str | None = None
    Option: int | None = None
    PreferredMoveBeginDateInUtc: datetime | None = field(default_factory=lambda: datetime.min)
    PreferredMoveEndDateInUtc: datetime | None = field(default_factory=lambda: datetime.min)
    Reserve: str | None = None
    SiteId: UUID | None = None
    SourceDataLocation: str | None = None
    State: int | None = None
    SubType: int | None = None
    TriggeredBy: str | None = None
    Type: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.MultiGeo.Service.SerilizableMoveJobEntityData"
