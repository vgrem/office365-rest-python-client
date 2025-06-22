from office365.runtime.client_value import ClientValue


class ActivityClientResponse(ClientValue):
    """"""

    def __init__(
        self, id_: str, message: str = None, server_id: str = None, status: int = None
    ) -> None:
        """ """
        self.id = id_
        self.message = message
        self.serverId = server_id
        self.status = status

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.ActivityClientResponse"
