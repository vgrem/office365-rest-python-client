from office365.runtime.client_value import ClientValue


class MigrationStorageSettings(ClientValue):

    def __init__(self, encrypted_certificate: str = None, encryption_key: str = None):
        self.EncryptedCertificate = encrypted_certificate
        self.EncryptionKey = encryption_key

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.MigrationStorageSettings"
