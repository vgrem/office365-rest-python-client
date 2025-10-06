from office365.runtime.client_value import ClientValue


class ItemReference(ClientValue):

    def __init__(self, exchange_id: str = None, site_id: str = None):
        self.exchangeId = exchange_id
        self.siteId = site_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.News.DataModel.ItemReference"
