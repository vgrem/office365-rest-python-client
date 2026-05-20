from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class DisplayNameLocalization(ClientValue):
    """Provides the ability for an administrator to customize the string used in a shared Microsoft 365 experience."""

    displayName: str | None = None
    languageTag: str | None = None
