from office365.runtime.client_value import ClientValue


class ProvisionChannelEmailResult(ClientValue):
    """Represents the email address provisioned for a channel."""

    def __init__(self, email=None):
        self.email = email
