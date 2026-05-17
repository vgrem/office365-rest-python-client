from typing import Optional

from typing_extensions import Self

from office365.runtime.paths.v3.static import StaticPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.social.thread import SocialThread


class SocialRestThread(Entity):
    """
    The SocialRestThread class specifies a thread that is stored on the server. The thread contains a root post
    and zero or more reply posts. The SocialRestThread type is available when the protocol client sends an OData
    request to a protocol server using [MS-CSOMREST]. It is not available using [MS-CSOM].
    """

    def __init__(self, context):
        super().__init__(context, StaticPath("SP.Social.SocialRestThread"))

    def like(self, post_id: str) -> Self:
        """
        The Like method makes the current user a liker of the specified post.

        :param str post_id: Specifies the post by its identifier.
        """
        payload = {"ID": post_id}
        qry = ServiceOperationQuery(self, "Like", None, payload, None, self)
        self.context.add_query(qry)
        return self

    def unlike(self, post_id: str) -> Self:
        """
        The Unlike method removes the current user from the list of likers for the specified post.
        If the current is not a liker of the post, this method has no effect.

        :param str post_id: Specifies the post by its identifier.
        """
        payload = {"ID": post_id}
        qry = ServiceOperationQuery(self, "UnLike", None, payload, None, self)
        self.context.add_query(qry)
        return self

    @property
    def social_thread(self) -> SocialThread:
        """The SocialThread property provides the object that contains the thread"""
        return self.properties.get("SocialThread", SocialThread())

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {"SocialThread": self.social_thread}
            default_value = property_mapping.get(name, None)
        return super().get_property(name, default_value)

    @property
    def id_(self) -> Optional[str]:
        """Gets the ID property"""
        return self.properties.get("ID", None)

    @property
    def entity_type_name(self):
        return "SP.Social.SocialRestThread"
