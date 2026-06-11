from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ExceptionDetails(ClientValue):
    ErrorCode: str | None = None
    IsExpectedException: bool | None = None
    Message: str | None = None
    StackTrace: str | None = None
