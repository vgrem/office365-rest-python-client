from office365.runtime.client_value import ClientValue


class SharingLinkExpirationAbilityStatus(ClientValue):
    def __init__(self, default_expiration_in_days: int = None):
        self.defaultExpirationInDays = default_expiration_in_days

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharingLinkExpirationAbilityStatus"
