from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ExceptionDetails(ClientValue):
    ErrorCode: str | None = None
    IsExpectedException: bool | None = None
    Message: str | None = None
    StackTrace: str | None = None
