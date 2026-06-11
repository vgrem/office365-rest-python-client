from __future__ import annotations

from office365.runtime.client_value import ClientValue


class BaseRequestParams(ClientValue):
    Top: int | None = None
