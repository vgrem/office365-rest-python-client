from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity
from office365.sharepoint.microfeed.link import MicrofeedLink


class MicrofeedAttachmentStore(Entity):
    def __init__(self, context):
        super().__init__(context, ResourcePath("SP.Microfeed.MicrofeedAttachmentStore"))

    @property
    def entity_type_name(self) -> str:
        return "SP.Microfeed.MicrofeedAttachmentStore"

    def delete_pre_processed_attachment(self, attachment_uri: str) -> Self:
        """DeletePreProcessedAttachment operation.

        Args:
            attachment_uri (str): attachmentUri parameter
        """
        qry = ServiceOperationQuery(
            self, "DeletePreProcessedAttachment", None, {"attachmentUri": attachment_uri}, None, None
        )
        self.context.add_query(qry)
        return self

    def get_image(self, image_url: str, key: str, iv: str) -> ClientResult[bytes]:
        """GetImage operation.

        Args:
            image_url (str): imageUrl parameter
            key (str): key parameter
            iv (str): iv parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = ServiceOperationQuery(
            self, "GetImage", None, {"imageUrl": image_url, "key": key, "iv": iv}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def pre_process_attachment(self, link: MicrofeedLink) -> ClientResult[MicrofeedLink]:
        """PreProcessAttachment operation.

        Args:
            link (MicrofeedLink): link parameter
        """
        return_type = ClientResult(self.context, MicrofeedLink())
        qry = ServiceOperationQuery(self, "PreProcessAttachment", None, {"link": link}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def put_file(self, original_file_name: str, file_data: bytes) -> ClientResult[StringCollection]:
        """PutFile operation.

        Args:
            original_file_name (str): originalFileName parameter
            file_data (bytes): fileData parameter
        """
        return_type = ClientResult(self.context, StringCollection())
        qry = ServiceOperationQuery(
            self, "PutFile", None, {"originalFileName": original_file_name, "fileData": file_data}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def put_image(self, image_data: bytes) -> ClientResult[StringCollection]:
        """PutImage operation.

        Args:
            image_data (bytes): imageData parameter
        """
        return_type = ClientResult(self.context, StringCollection())
        qry = ServiceOperationQuery(self, "PutImage", None, {"imageData": image_data}, None, return_type)
        self.context.add_query(qry)
        return return_type
