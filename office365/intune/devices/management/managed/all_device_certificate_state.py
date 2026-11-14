from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class ManagedAllDeviceCertificateState(Entity):
    @odata(name="certificateExpirationDateTime")
    @property
    def certificate_expiration_date_time(self) -> Optional[datetime]:
        """Gets the certificateExpirationDateTime property"""
        return self.properties.get("certificateExpirationDateTime", None)

    @odata(name="certificateExtendedKeyUsages")
    @property
    def certificate_extended_key_usages(self) -> Optional[str]:
        """Gets the certificateExtendedKeyUsages property"""
        return self.properties.get("certificateExtendedKeyUsages", None)

    @odata(name="certificateIssuanceDateTime")
    @property
    def certificate_issuance_date_time(self) -> Optional[datetime]:
        """Gets the certificateIssuanceDateTime property"""
        return self.properties.get("certificateIssuanceDateTime", None)

    @odata(name="certificateIssuerName")
    @property
    def certificate_issuer_name(self) -> Optional[str]:
        """Gets the certificateIssuerName property"""
        return self.properties.get("certificateIssuerName", None)

    @odata(name="certificateKeyUsages")
    @property
    def certificate_key_usages(self) -> Optional[int]:
        """Gets the certificateKeyUsages property"""
        return self.properties.get("certificateKeyUsages", None)

    @odata(name="certificateRevokeStatusLastChangeDateTime")
    @property
    def certificate_revoke_status_last_change_date_time(self) -> Optional[datetime]:
        """Gets the certificateRevokeStatusLastChangeDateTime property"""
        return self.properties.get("certificateRevokeStatusLastChangeDateTime", None)

    @odata(name="certificateSerialNumber")
    @property
    def certificate_serial_number(self) -> Optional[str]:
        """Gets the certificateSerialNumber property"""
        return self.properties.get("certificateSerialNumber", None)

    @odata(name="certificateSubjectName")
    @property
    def certificate_subject_name(self) -> Optional[str]:
        """Gets the certificateSubjectName property"""
        return self.properties.get("certificateSubjectName", None)

    @odata(name="certificateThumbprint")
    @property
    def certificate_thumbprint(self) -> Optional[str]:
        """Gets the certificateThumbprint property"""
        return self.properties.get("certificateThumbprint", None)

    @odata(name="managedDeviceDisplayName")
    @property
    def managed_device_display_name(self) -> Optional[str]:
        """Gets the managedDeviceDisplayName property"""
        return self.properties.get("managedDeviceDisplayName", None)

    @odata(name="userPrincipalName")
    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the userPrincipalName property"""
        return self.properties.get("userPrincipalName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ManagedAllDeviceCertificateState"
