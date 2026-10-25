from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class LogFileInfo(Entity):
    @odata(name="AlternateUrl")
    @property
    def alternate_url(self) -> Optional[str]:
        """Gets the AlternateUrl property"""
        return self.properties.get("AlternateUrl", None)

    @odata(name="DecryptionIV")
    @property
    def decryption_iv(self) -> Optional[bytes]:
        """Gets the DecryptionIV property"""
        return self.properties.get("DecryptionIV", None)

    @odata(name="DecryptionKey")
    @property
    def decryption_key(self) -> Optional[bytes]:
        """Gets the DecryptionKey property"""
        return self.properties.get("DecryptionKey", None)

    @odata(name="Exception")
    @property
    def exception(self) -> Optional[str]:
        """Gets the Exception property"""
        return self.properties.get("Exception", None)

    @odata(name="FileName")
    @property
    def file_name(self) -> Optional[str]:
        """Gets the FileName property"""
        return self.properties.get("FileName", None)

    @odata(name="Url")
    @property
    def url(self) -> Optional[str]:
        """Gets the Url property"""
        return self.properties.get("Url", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.SPLogger.LogFileInfo"
