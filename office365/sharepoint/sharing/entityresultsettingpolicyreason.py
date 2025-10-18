from office365.runtime.client_value import ClientValue


class SharingEntityResultSettingPolicyReason(ClientValue):

    def __init__(
        self,
        setting_policy_result: int = None,
        setting_policy_result_string: str = None,
    ):
        self.SettingPolicyResult = setting_policy_result
        self.SettingPolicyResultString = setting_policy_result_string

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingEntityResultSettingPolicyReason"
