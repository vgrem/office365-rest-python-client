from office365.runtime.client_value import ClientValue


class RestoreVersionFacet(ClientValue):
    def __init__(self, from_version: str = None):
        self.fromVersion = from_version

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.RestoreVersionFacet"
