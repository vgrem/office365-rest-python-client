from office365.runtime.client_value import ClientValue


class SPUninstallAddinErrorDetail(ClientValue):

    def __init__(
        self,
        correlation_id: str = None,
        detail: str = None,
        exception_message: str = None,
        source: str = None,
        type_: str = None,
    ):
        self.correlationId = correlation_id
        self.detail = detail
        self.exceptionMessage = exception_message
        self.source = source
        self.type = type_

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPUninstallAddinErrorDetail"
