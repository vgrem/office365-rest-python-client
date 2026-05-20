from __future__ import annotations

from dataclasses import dataclass

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
