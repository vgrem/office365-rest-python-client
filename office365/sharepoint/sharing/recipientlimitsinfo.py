from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class RecipientLimitsInfo(ClientValue):
    alias_only: int | None = None
    email_only: int | None = None
    mixed_recipients: int | None = None
    object_id_only: int | None = None
