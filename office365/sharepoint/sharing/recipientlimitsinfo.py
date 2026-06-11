from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class RecipientLimitsInfo(ClientValue):
    AliasOnly: int | None = None
    EmailOnly: int | None = None
    MixedRecipients: int | None = None
    ObjectIdOnly: int | None = None
