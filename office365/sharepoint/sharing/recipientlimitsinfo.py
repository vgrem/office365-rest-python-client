from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class RecipientLimitsInfo(ClientValue):
    AliasOnly: int | None = None
    EmailOnly: int | None = None
    MixedRecipients: int | None = None
    ObjectIdOnly: int | None = None
