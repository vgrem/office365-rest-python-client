from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue


@dataclass
class TranspilerStatement(ClientValue):
    Arguments: dict = field(default_factory=dict)
    Returns: str | None = None
    StatementName: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.Copilot.TranspilerStatement"
