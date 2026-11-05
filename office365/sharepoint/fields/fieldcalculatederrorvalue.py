from __future__ import annotations

from office365.runtime.client_value import ClientValue


class FieldCalculatedErrorValue(ClientValue):
    ErrorMessage: str | None = None
