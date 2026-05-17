from typing import Optional

from office365.runtime.client_value import ClientValue


class SPUninstallAddinErrorDetail(ClientValue):
    def __init__(
        self,
        correlation_id: Optional[str] = None,
        detail: Optional[str] = None,
        exception_message: Optional[str] = None,
        source: Optional[str] = None,
        type_: Optional[str] = None,
    ):
        self.correlationId = correlation_id
        self.detail = detail
        self.exceptionMessage = exception_message
        self.source = source
        self.type = type_

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPUninstallAddinErrorDetail"
