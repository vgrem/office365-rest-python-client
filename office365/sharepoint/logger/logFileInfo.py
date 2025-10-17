from typing import Optional

from office365.sharepoint.entity import Entity


class LogFileInfo(Entity):

    @property
    def alternate_url(self) -> Optional[str]:
        """Gets the AlternateUrl property"""
        return self.properties.get("AlternateUrl", None)

    @property
    def decryption_iv(self) -> Optional[bytes]:
        """Gets the DecryptionIV property"""
        return self.properties.get("DecryptionIV", None)

    @property
    def decryption_key(self) -> Optional[bytes]:
        """Gets the DecryptionKey property"""
        return self.properties.get("DecryptionKey", None)

    @property
    def exception(self) -> Optional[str]:
        """Gets the Exception property"""
        return self.properties.get("Exception", None)

    @property
    def file_name(self) -> Optional[str]:
        """Gets the FileName property"""
        return self.properties.get("FileName", None)

    @property
    def url(self) -> Optional[str]:
        """Gets the Url property"""
        return self.properties.get("Url", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.SPLogger.LogFileInfo"
