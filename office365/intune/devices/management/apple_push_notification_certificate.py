from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class ApplePushNotificationCertificate(Entity):
    @odata(name="appleIdentifier")
    @property
    def apple_identifier(self) -> Optional[str]:
        """Gets the appleIdentifier property"""
        return self.properties.get("appleIdentifier", None)

    @odata(name="certificate")
    @property
    def certificate(self) -> Optional[str]:
        """Gets the certificate property"""
        return self.properties.get("certificate", None)

    @odata(name="certificateSerialNumber", readonly=True)
    @property
    def certificate_serial_number(self) -> Optional[str]:
        """Gets the certificateSerialNumber property"""
        return self.properties.get("certificateSerialNumber", None)

    @odata(name="certificateUploadFailureReason")
    @property
    def certificate_upload_failure_reason(self) -> Optional[str]:
        """Gets the certificateUploadFailureReason property"""
        return self.properties.get("certificateUploadFailureReason", None)

    @odata(name="certificateUploadStatus")
    @property
    def certificate_upload_status(self) -> Optional[str]:
        """Gets the certificateUploadStatus property"""
        return self.properties.get("certificateUploadStatus", None)

    @odata(name="expirationDateTime")
    @property
    def expiration_date_time(self) -> Optional[datetime]:
        """Gets the expirationDateTime property"""
        return self.properties.get("expirationDateTime", datetime.min)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="topicIdentifier")
    @property
    def topic_identifier(self) -> Optional[str]:
        """Gets the topicIdentifier property"""
        return self.properties.get("topicIdentifier", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ApplePushNotificationCertificate"
