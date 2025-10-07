from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.identity.spdefaultdocumentlibrary import (
    SPDefaultDocumentLibrary,
)


class SPRubySite(ClientValue):

    def __init__(
        self,
        channel_group_id: str = None,
        created_date_time: datetime = None,
        default_document_library: SPDefaultDocumentLibrary = SPDefaultDocumentLibrary(),
        description: str = None,
        id_: str = None,
        last_modified_date_time: datetime = None,
        name: str = None,
        web_url: str = None,
    ):
        self.channelGroupId = channel_group_id
        self.createdDateTime = created_date_time
        self.defaultDocumentLibrary = default_document_library
        self.description = description
        self.id = id_
        self.lastModifiedDateTime = last_modified_date_time
        self.name = name
        self.webUrl = web_url

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.IdentityModel.SPRubySite"
