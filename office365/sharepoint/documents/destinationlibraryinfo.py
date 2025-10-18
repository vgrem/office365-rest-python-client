from office365.runtime.client_value import ClientValue


class DestinationLibraryInfo(ClientValue):

    def __init__(self, library_id: str = None, site_id: str = None, web_id: str = None):
        self.LibraryId = library_id
        self.SiteId = site_id
        self.WebId = web_id
