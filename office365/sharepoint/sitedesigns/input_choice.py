from __future__ import annotations

from office365.runtime.client_value import ClientValue


class InputChoice(ClientValue):
    isSelected: bool | None = None
    title: str | None = None
    value: str | None = None
