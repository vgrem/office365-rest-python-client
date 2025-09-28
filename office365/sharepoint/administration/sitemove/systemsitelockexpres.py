from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SystemSiteLockExpirationResult(ClientValue):
    """"""

    def __init__(self, error=None, expiration=None):
        self.Error = error
        self.Expiration = expiration
