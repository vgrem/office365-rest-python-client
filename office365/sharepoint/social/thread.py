from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.social.actor import SocialActor
from office365.sharepoint.social.posts.post import SocialPost
from office365.sharepoint.social.posts.reference import SocialPostReference


class SocialThread(ClientValue):
    """The SocialThread property provides the object that contains the thread.
    For details on the SocialThread type, see section 3.1.5.42."""

    def __init__(
        self,
        actors=None,
        replies=None,
        root_post=SocialPost(),
        post_reference=SocialPostReference(),
        attributes: int = None,
        id_: str = None,
        owner_index: int = None,
        permalink: str = None,
        status: int = None,
        thread_type: int = None,
        total_reply_count: int = None,
    ):
        """
        :param str thread_id: The Id property specifies the unique identification of the thread.
        :param list[SocialActor] actors: The Actors property is an array that specifies the users who have created
            a post in the returned thread and also contains any users, documents, sites, and tags that are referenced
            in any of the posts in the returned thread.
        :param list[SocialPost] replies: The Replies property returns an array of zero or more reply posts.
            The server can return a subset of the reply posts that are stored on the server.
        :param SocialPost root_post: The RootPost property returns the root post.
        :param SocialPostReference post_reference:
        """
        self.Actors = ClientValueCollection(SocialActor, actors)
        self.RootPost = root_post
        self.Replies = ClientValueCollection(SocialPost, replies)
        self.PostReference = post_reference
        self.Attributes = attributes
        self.Id = id_
        self.OwnerIndex = owner_index
        self.Permalink = permalink
        self.Status = status
        self.ThreadType = thread_type
        self.TotalReplyCount = total_reply_count

    @property
    def entity_type_name(self):
        return "SP.Social.SocialThread"
