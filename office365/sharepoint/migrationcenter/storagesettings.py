from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class MigrationStorageSettings(ClientValue):
    EncryptedCertificate: Optional[str] = None
    EncryptionKey: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.MigrationStorageSettings"
