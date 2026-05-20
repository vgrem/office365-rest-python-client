from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SharingEntityResultSettingPolicyReason(ClientValue):
    SettingPolicyResult: int | None = None
    SettingPolicyResultString: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingEntityResultSettingPolicyReason"
