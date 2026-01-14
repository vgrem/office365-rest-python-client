from office365.runtime.client_value import ClientValue


class ErrorFacet(ClientValue):
    def __init__(self, code: str = None, message: str = None):
        self.Code = code
        self.Message = message

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.ErrorFacet"
