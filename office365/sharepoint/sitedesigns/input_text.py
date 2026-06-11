from __future__ import annotations

from office365.runtime.client_value import ClientValue


class InputText(ClientValue):
    isMultiline: bool | None = None
    isRequired: bool | None = None
    maxLength: int | None = None
    placeholder: str | None = None
    style: str | None = None
