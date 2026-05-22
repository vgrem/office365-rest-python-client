from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.hunting_row_result import HuntingRowResult
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class HuntingQueryResults(ClientValue):
    """The results of running a query for advanced hunting."""

    results: ClientValueCollection[HuntingRowResult] = field(
        default_factory=lambda: ClientValueCollection(HuntingRowResult)
    )
