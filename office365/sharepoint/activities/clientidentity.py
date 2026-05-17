from typing import Optional

from office365.runtime.client_value import ClientValue


class ActivityClientIdentity(ClientValue):
    def __init__(
        self,
        email: Optional[str] = None,
        name: Optional[str] = None,
        id_: Optional[str] = None,
        provider: Optional[str] = None,
    ):
        self.email = email
        self.name = name
        self.id = id_
        self.provider = provider

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.ActivityClientIdentity"
