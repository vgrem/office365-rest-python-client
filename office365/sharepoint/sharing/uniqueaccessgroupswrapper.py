from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.uniqueaccessgroupinfo import UniqueAccessGroupInfo


class UniqueAccessGroupsWrapper(ClientValue):

    def __init__(
        self,
        discoverable_by_organization: UniqueAccessGroupInfo = UniqueAccessGroupInfo(),
    ):
        self.discoverableByOrganization = discoverable_by_organization

    @property
    def entity_type_name(self):
        return "SP.Sharing.UniqueAccessGroupsWrapper"
