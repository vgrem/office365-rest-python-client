from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenant.administration.container.filterorder import (
    SPContainerFilterOrder,
)
from office365.sharepoint.tenant.administration.container.sortorder import (
    SPContainerSortOrder,
)


class SPOContainerQueryParams(ClientValue):
    def __init__(
        self,
        filter_by_columns_list: ClientValueCollection[SPContainerFilterOrder] = ClientValueCollection(
            SPContainerFilterOrder
        ),
        order_by_columns_list: ClientValueCollection[SPContainerSortOrder] = ClientValueCollection(SPContainerSortOrder),
        paging_token: str = None,
    ):
        self.FilterByColumnsList = filter_by_columns_list
        self.OrderByColumnsList = order_by_columns_list
        self.PagingToken = paging_token

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOContainerQueryParams"
