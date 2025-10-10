from office365.runtime.client_value import ClientValue


class VersionFacet(ClientValue):
    """"""

    def __init__(self, fromVersion=None, new_version: str = None):
        self.fromVersion = fromVersion
        self.newVersion = new_version

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.VersionFacet"
