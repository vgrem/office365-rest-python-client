from office365.runtime.client_value import ClientValue


class SocialActorInfo(ClientValue):
    """The SocialActorInfo type identifies an actor to the server. An actor can be a user, document, site, or tag."""

    def __init__(
        self,
        account_name=None,
        actor_type: int = None,
        content_uri: str = None,
        id_: str = None,
        tag_guid: str = None,
    ):
        """
        :param str account_name: The AccountName property specifies the user's account name. Users can be identified
            by this property.
        """
        self.AccountName = account_name
        self.ActorType = actor_type
        self.ContentUri = content_uri
        self.Id = id_
        self.TagGuid = tag_guid

    @property
    def entity_type_name(self):
        return "SP.Social.SocialActorInfo"
