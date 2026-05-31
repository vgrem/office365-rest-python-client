from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class IdleSessionSignOut(ClientValue):
    """Represents the idle session sign-out policy settings for SharePoint."""

    isEnabled: bool | None = None
    signOutAfterInSeconds: int | None = None
    warnAfterInSeconds: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IdleSessionSignOut"
