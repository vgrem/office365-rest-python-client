from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class UsageInfo(ClientValue):
    """Provides fields used to access information regarding site collection usage.

    Fields:
        Bandwidth: Contains the cumulative bandwidth used by the site collection on the previous day or
            on the last day that log files were processed, which is tracked by usage analysis code.
        DiscussionStorage: Contains the amount of storage, identified in bytes,
            used by Web discussion data in the site collection.
        Visits: Contains the cumulative number of visits to the site collection,
            which is tracked by the usage analysis code.
    """

    Bandwidth: Optional[int] = None
    DiscussionStorage: Optional[int] = None
    Visits: Optional[int] = None
    Hits: Optional[int] = None
    Storage: Optional[int] = None
    StoragePercentageUsed: Optional[float] = None
