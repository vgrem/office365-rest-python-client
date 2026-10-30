from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.partners.billing.blob import Blob
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata


class Manifest(Entity):
    @odata(name="blobCount")
    @property
    def blob_count(self) -> Optional[int]:
        """Gets the blobCount property"""
        return self.properties.get("blobCount", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="dataFormat")
    @property
    def data_format(self) -> Optional[str]:
        """Gets the dataFormat property"""
        return self.properties.get("dataFormat", None)

    @odata(name="eTag")
    @property
    def e_tag(self) -> Optional[str]:
        """Gets the eTag property"""
        return self.properties.get("eTag", None)

    @odata(name="partitionType")
    @property
    def partition_type(self) -> Optional[str]:
        """Gets the partitionType property"""
        return self.properties.get("partitionType", None)

    @odata(name="partnerTenantId")
    @property
    def partner_tenant_id(self) -> Optional[str]:
        """Gets the partnerTenantId property"""
        return self.properties.get("partnerTenantId", None)

    @odata(name="rootDirectory")
    @property
    def root_directory(self) -> Optional[str]:
        """Gets the rootDirectory property"""
        return self.properties.get("rootDirectory", None)

    @odata(name="sasToken")
    @property
    def sas_token(self) -> Optional[str]:
        """Gets the sasToken property"""
        return self.properties.get("sasToken", None)

    @odata(name="schemaVersion")
    @property
    def schema_version(self) -> Optional[str]:
        """Gets the schemaVersion property"""
        return self.properties.get("schemaVersion", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.partners.billing.Manifest"

    @odata(name="blobs")
    @property
    def blobs(self) -> ClientValueCollection[Blob]:
        """Gets the blobs property"""
        return self.properties.get("blobs", ClientValueCollection[Blob](Blob))
