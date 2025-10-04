from datetime import datetime

from office365.runtime.client_value import ClientValue


class SitePageVersionInfoCollection(ClientValue):

    def __init__(self, created: datetime = None, created_by: str = None):
        self.Created = created
        self.CreatedBy = created_by
