from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class CountByDate(ClientValue):
    count: Optional[int] = None
    date: Optional[int] = None
