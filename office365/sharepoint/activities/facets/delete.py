from office365.runtime.client_value import ClientValue


class DeleteFacet(ClientValue):
    """"""

    def __init__(self, name: str = None) -> None:
        self.name = name

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.DeleteFacet"
