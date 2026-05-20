from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SocialActorInfo(ClientValue):
    """The SocialActorInfo type identifies an actor to the server. An actor can be a user, document, site, or tag.

    Fields:
        AccountName (str, optional): The AccountName property specifies the user's account name. Users can be identified
            by this property.
    """

    AccountName: Optional[str] = None
    ActorType: Optional[int] = None
    ContentUri: Optional[str] = None
    Id: Optional[str] = None
    TagGuid: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Social.SocialActorInfo"
