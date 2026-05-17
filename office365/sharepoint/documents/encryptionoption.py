from typing import Optional

from office365.runtime.client_value import ClientValue


class EncryptionOption(ClientValue):
    def __init__(self, aes256_cbc_key: Optional[bytes] = None):
        self.aes256_cbc_key = aes256_cbc_key
