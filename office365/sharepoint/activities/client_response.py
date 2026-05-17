from typing import Optional

from office365.runtime.client_value import ClientValue


class ActivityClientResponse(ClientValue):
    """"""

    def __init__(
        self, id_: str, message: Optional[str] = None, server_id: Optional[str] = None, status: Optional[int] = None
    ) -> None:
        """ """
        self.id = id_
        self.message = message
        self.serverId = server_id
        self.status = status

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.ActivityClientResponse"
