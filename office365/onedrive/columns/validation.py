from __future__ import annotations

from dataclasses import dataclass, field

from office365.onedrive.columns.display_name_localization import DisplayNameLocalization
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class ColumnValidation(ClientValue):
    """Represents properties that validates column values."""

    formula: str | None = None
    descriptions: ClientValueCollection = field(
        default_factory=lambda: ClientValueCollection(DisplayNameLocalization)
    )
    defaultLanguage: str | None = None
