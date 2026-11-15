from __future__ import annotations

from dataclasses import field

from office365.security.alerts.evidence.base import AlertEvidence
from office365.security.alerts.user_account import UserAccount
from office365.security.stream import Stream


class UserEvidence(AlertEvidence):
    stream: Stream = field(default_factory=Stream)
    userAccount: UserAccount = field(default_factory=UserAccount)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.UserEvidence"
