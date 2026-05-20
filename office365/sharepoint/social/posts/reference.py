from dataclasses import dataclass, field
from typing import Any, Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.social.posts.post import SocialPost


@dataclass
class SocialPostReference(ClientValue):
    """The SocialPostReference class specifies a reference to a post in another thread.  The referenced post can be a
    post with a tag, a post that is liked, a post that mentions a user, or a post that is a reply. Threads that contain
    a SocialPostReference in the PostReference property (see section 3.1.5.42.1.1.6) are threads with root posts that
    are generated on the server and not created by a client.

    Fields:
        Digest (SocialThread, optional): The Digest property provides a digest of the thread containing the
            referenced post.
        Post (SocialPost, optional): The Post property provides access to the post being referenced.
        ThreadId (str, optional): The ThreadId property specifies the unique identifier of the thread containing the
            referenced post.
        ThreadOwnerIndex (int, optional): The ThreadOwnerIndex property specifies the current owner of the thread as an
            index into the SocialThread Actors array.
    """

    Digest: Any = None
    Post: SocialPost = field(default_factory=SocialPost)
    ThreadId: Optional[str] = None
    ThreadOwnerIndex: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Social.SocialPostReference"
