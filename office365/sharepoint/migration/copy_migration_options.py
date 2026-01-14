from office365.runtime.client_value import ClientValue


class CopyMigrationOptions(ClientValue):
    """ """

    def __init__(
        self,
        allow_schema_mismatch=None,
        allow_smaller_version_limit_on_destination=None,
        bypass_shared_lock=None,
        client_etags=None,
    ):
        self.AllowSchemaMismatch = allow_schema_mismatch
        self.AllowSmallerVersionLimitOnDestination = allow_smaller_version_limit_on_destination
        self.BypassSharedLock = bypass_shared_lock
        self.ClientEtags = client_etags
