from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class SPMachineLearningSample(Entity):
    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SPMachineLearningSample"

    @odata(name="Created", beta=True)
    @property
    def created(self) -> Optional[datetime]:
        """Gets the Created property"""
        return self.properties.get("Created", datetime.min)

    @odata(name="CreatedBy", beta=True)
    @property
    def created_by(self) -> Optional[str]:
        """Gets the CreatedBy property"""
        return self.properties.get("CreatedBy", None)

    @odata(name="CreatedByName", beta=True)
    @property
    def created_by_name(self) -> Optional[str]:
        """Gets the CreatedByName property"""
        return self.properties.get("CreatedByName", None)

    @odata(name="DriveId", beta=True)
    @property
    def drive_id(self) -> Optional[str]:
        """Gets the DriveId property"""
        return self.properties.get("DriveId", None)

    @odata(name="Etag", beta=True)
    @property
    def etag(self) -> Optional[str]:
        """Gets the Etag property"""
        return self.properties.get("Etag", None)

    @odata(name="ExtractedText", beta=True)
    @property
    def extracted_text(self) -> Optional[str]:
        """Gets the ExtractedText property"""
        return self.properties.get("ExtractedText", None)

    @odata(name="FileLeafRef", beta=True)
    @property
    def file_leaf_ref(self) -> Optional[str]:
        """Gets the FileLeafRef property"""
        return self.properties.get("FileLeafRef", None)

    @odata(name="FileRef", beta=True)
    @property
    def file_ref(self) -> Optional[str]:
        """Gets the FileRef property"""
        return self.properties.get("FileRef", None)

    @odata(name="FileType", beta=True)
    @property
    def file_type(self) -> Optional[str]:
        """Gets the FileType property"""
        return self.properties.get("FileType", None)

    @odata(name="FSObjType", beta=True)
    @property
    def fs_obj_type(self) -> Optional[int]:
        """Gets the FSObjType property"""
        return self.properties.get("FSObjType", None)

    @odata(name="ID", beta=True)
    @property
    def id_(self) -> Optional[int]:
        """Gets the ID property"""
        return self.properties.get("ID", None)

    @odata(name="ListID", beta=True)
    @property
    def list_id(self) -> Optional[UUID]:
        """Gets the ListID property"""
        return self.properties.get("ListID", None)

    @odata(name="Markups", beta=True)
    @property
    def markups(self) -> Optional[str]:
        """Gets the Markups property"""
        return self.properties.get("Markups", None)

    @odata(name="ModelIds", beta=True)
    @property
    def model_ids(self) -> ClientValueCollection:
        """Gets the ModelIds property"""
        return self.properties.get("ModelIds", ClientValueCollection(int))

    @odata(name="Modified", beta=True)
    @property
    def modified(self) -> Optional[datetime]:
        """Gets the Modified property"""
        return self.properties.get("Modified", datetime.min)

    @odata(name="ModifiedBy", beta=True)
    @property
    def modified_by(self) -> Optional[str]:
        """Gets the ModifiedBy property"""
        return self.properties.get("ModifiedBy", None)

    @odata(name="ModifiedByName", beta=True)
    @property
    def modified_by_name(self) -> Optional[str]:
        """Gets the ModifiedByName property"""
        return self.properties.get("ModifiedByName", None)

    @odata(name="ObjectId", beta=True)
    @property
    def object_id(self) -> Optional[str]:
        """Gets the ObjectId property"""
        return self.properties.get("ObjectId", None)

    @odata(name="ServerRedirectedEmbedUri", beta=True)
    @property
    def server_redirected_embed_uri(self) -> Optional[str]:
        """Gets the ServerRedirectedEmbedUri property"""
        return self.properties.get("ServerRedirectedEmbedUri", None)

    @odata(name="Title", beta=True)
    @property
    def title(self) -> Optional[str]:
        """Gets the Title property"""
        return self.properties.get("Title", None)

    @odata(name="TokenEndPosition", beta=True)
    @property
    def token_end_position(self) -> ClientValueCollection:
        """Gets the TokenEndPosition property"""
        return self.properties.get("TokenEndPosition", ClientValueCollection(int))

    @odata(name="TokenStartPosition", beta=True)
    @property
    def token_start_position(self) -> ClientValueCollection:
        """Gets the TokenStartPosition property"""
        return self.properties.get("TokenStartPosition", ClientValueCollection(int))

    @odata(name="UniqueId", beta=True)
    @property
    def unique_id(self) -> Optional[UUID]:
        """Gets the UniqueId property"""
        return self.properties.get("UniqueId", None)

    @odata(name="ID", beta=True)
    @property
    def id(self) -> Optional[int]:
        """Gets the ID property"""
        return self.properties.get("ID", None)
