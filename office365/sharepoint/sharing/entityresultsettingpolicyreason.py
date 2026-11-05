from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SharingEntityResultSettingPolicyReason(ClientValue):
    SettingPolicyResult: int | None = None
    SettingPolicyResultString: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingEntityResultSettingPolicyReason"
