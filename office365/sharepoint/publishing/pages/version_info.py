from datetime import datetime

from office365.runtime.client_value import ClientValue


class SitePageVersionInfo(ClientValue):
    def __init__(self, last_version_created: datetime = None, last_version_created_by: str = None):
        """Represents the version information for a given SitePage."""
        self.LastVersionCreated = last_version_created
        self.LastVersionCreatedBy = last_version_created_by

    @property
    def entity_type_name(self):
        return "SP.Publishing.SitePageVersionInfo"
