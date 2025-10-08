from office365.runtime.client_value import ClientValue


class SPClientSideComponentIdentifier(ClientValue):
    """This identifier uniquely identifies a component."""

    def __init__(self, _id=None, version=None, id_: str = None):
        self.id = _id
        self.version = version
        self.id = id_

    def __repr__(self):
        return self.id or self.entity_type_name

    @property
    def entity_type_name(self):
        return (
            "Microsoft.SharePoint.ClientSideComponent.SPClientSideComponentIdentifier"
        )
