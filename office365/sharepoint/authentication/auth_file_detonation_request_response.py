from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class AuthFileDetonationRequestResponse(Entity):
    @odata(name="correlationId")
    @property
    def correlation_id(self) -> Optional[str]:
        """Gets the correlationId property"""
        return self.properties.get("correlationId", None)

    @odata(name="documentId")
    @property
    def document_id(self) -> Optional[UUID]:
        """Gets the documentId property"""
        return self.properties.get("documentId", None)

    @odata(name="failureReason")
    @property
    def failure_reason(self) -> Optional[int]:
        """Gets the failureReason property"""
        return self.properties.get("failureReason", None)

    @odata(name="fileETag")
    @property
    def file_e_tag(self) -> Optional[str]:
        """Gets the fileETag property"""
        return self.properties.get("fileETag", None)

    @odata(name="prevDetonationToken")
    @property
    def prev_detonation_token(self) -> Optional[str]:
        """Gets the prevDetonationToken property"""
        return self.properties.get("prevDetonationToken", None)

    @odata(name="siteId")
    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the siteId property"""
        return self.properties.get("siteId", None)

    @odata(name="spoCloud")
    @property
    def spo_cloud(self) -> Optional[str]:
        """Gets the spoCloud property"""
        return self.properties.get("spoCloud", None)

    @odata(name="spoRegion")
    @property
    def spo_region(self) -> Optional[str]:
        """Gets the spoRegion property"""
        return self.properties.get("spoRegion", None)

    @odata(name="authZFailureReason")
    @property
    def auth_z_failure_reason(self) -> Optional[str]:
        """Gets the authZFailureReason property"""
        return self.properties.get("authZFailureReason", None)

    @odata(name="authZResult")
    @property
    def auth_z_result(self) -> Optional[str]:
        """Gets the authZResult property"""
        return self.properties.get("authZResult", None)

    @odata(name="storageSignal")
    @property
    def storage_signal(self) -> Optional[str]:
        """Gets the storageSignal property"""
        return self.properties.get("storageSignal", None)
