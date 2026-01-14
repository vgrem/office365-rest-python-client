from datetime import datetime

from office365.runtime.client_value import ClientValue


class SPDefaultDocumentLibrary(ClientValue):
    def __init__(self, last_modified_by: str = None, last_modified_date_time: datetime = None):
        self.lastModifiedBy = last_modified_by
        self.lastModifiedDateTime = last_modified_date_time

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.IdentityModel.SPDefaultDocumentLibrary"
