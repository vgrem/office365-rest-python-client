from __future__ import annotations

from dataclasses import dataclass, field

from office365.onedrive.storage_plan_information import StoragePlanInformation
from office365.runtime.client_value import ClientValue


@dataclass
class Quota(ClientValue):
    """
    The quota resource provides details about space constraints on a drive resource.
    In OneDrive Personal, the values reflect the total/used unified storage quota across multiple Microsoft services.
    """

    deleted: int | None = None
    remaining: int | None = None
    state: str | None = None
    total: int | None = None
    used: int | None = None
    storagePlanInformation: StoragePlanInformation = field(default_factory=StoragePlanInformation)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Quota"
