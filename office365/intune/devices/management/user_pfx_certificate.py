from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class UserPFXCertificate(Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", None)

    @odata(name="encryptedPfxBlob")
    @property
    def encrypted_pfx_blob(self) -> Optional[bytes]:
        """Gets the encryptedPfxBlob property"""
        return self.properties.get("encryptedPfxBlob", None)

    @odata(name="encryptedPfxPassword")
    @property
    def encrypted_pfx_password(self) -> Optional[str]:
        """Gets the encryptedPfxPassword property"""
        return self.properties.get("encryptedPfxPassword", None)

    @odata(name="expirationDateTime")
    @property
    def expiration_date_time(self) -> Optional[datetime]:
        """Gets the expirationDateTime property"""
        return self.properties.get("expirationDateTime", None)

    @odata(name="keyName")
    @property
    def key_name(self) -> Optional[str]:
        """Gets the keyName property"""
        return self.properties.get("keyName", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="providerName")
    @property
    def provider_name(self) -> Optional[str]:
        """Gets the providerName property"""
        return self.properties.get("providerName", None)

    @odata(name="startDateTime")
    @property
    def start_date_time(self) -> Optional[datetime]:
        """Gets the startDateTime property"""
        return self.properties.get("startDateTime", None)

    @odata(name="thumbprint")
    @property
    def thumbprint(self) -> Optional[str]:
        """Gets the thumbprint property"""
        return self.properties.get("thumbprint", None)

    @odata(name="userPrincipalName")
    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the userPrincipalName property"""
        return self.properties.get("userPrincipalName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserPFXCertificate"
