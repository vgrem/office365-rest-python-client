from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class LocalizedLabel(ClientValue):
    """
    Represents the localized name used in the term store, which identifies the name in the localized language.
    For more information, see localizedLabel.

    Sentinel for a payload: no OData type name is declared, for the same measured reason as
    :class:`~office365.onedrive.termstore.sets.name.LocalizedName` - the term store refuses a
    cast here too ("[termModel] The specified type named ... is not recognized").
    """

    name: str | None = None
    languageTag: str = "en-US"
    isDefault: bool = True
