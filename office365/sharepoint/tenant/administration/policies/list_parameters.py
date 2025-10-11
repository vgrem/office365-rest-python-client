from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPOListParameters(ClientValue):

    def __init__(self, id_: UUID = None, title: str = None):
        self.Id = id_
        self.Title = title

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOListParameters"
