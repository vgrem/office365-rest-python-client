from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SyntexCustomModelDeploymentModelInfo(ClientValue):
    Format: str | None = None
    Name: str | None = None
    SourceAccount: str | None = None
    Version: str | None = None
