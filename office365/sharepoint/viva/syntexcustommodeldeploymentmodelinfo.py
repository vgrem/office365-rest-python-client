from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SyntexCustomModelDeploymentModelInfo(ClientValue):
    Format: str | None = None
    Name: str | None = None
    SourceAccount: str | None = None
    Version: str | None = None
