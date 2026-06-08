from typing import Optional

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.social.actor import SocialActor
from office365.sharepoint.social.attachment import SocialAttachment
from office365.sharepoint.social.feed.feed import SocialFeed
from office365.sharepoint.social.posts.creation_data import SocialPostCreationData
from office365.sharepoint.social.thread import SocialThread


class SocialFeedManager(Entity):
    """The SocialFeedManager class provides access to social feeds. It provides methods to create posts,
    delete posts, read posts, and perform other operations on posts."""

    def __init__(self, context, resource_path=None):
        if resource_path is None:
            resource_path = ResourcePath("SP.Social.SocialFeedManager")
        super().__init__(context, resource_path)

    def create_post(self, target_id: Optional[str] = None, creation_data: Optional[SocialPostCreationData] = None):
        """The CreatePost method creates a post in the current user's feed, in the specified user's feed, or in
        the specified thread. This method returns a new or a modified thread.

        Args:
            target_id (str or None): Optional, specifies the target of the post. If this parameter is null, the post is created as a root post in the current user's feed. If this parameter is set to a site (2) URL or a site (2) actor identification, the post is created as a root post in the specified site (2) feed. If this parameter is set to a thread identification, the post is created as a reply post in the specified thread.
            creation_data (SocialPostCreationData): Specifies the text and details of the post.
        """
        return_type = ClientResult(self.context, SocialThread())
        payload = {"targetId": target_id, "creationData": creation_data}
        qry = ServiceOperationQuery(self, "CreatePost", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def delete_post(self, post_id: str) -> ClientResult[SocialThread]:
        """The DeletePost method deletes the specified post. This method returns a digest of the modified thread.
        If the entire thread is deleted, this method returns null.

        Args:
            post_id (str): Specifies the post to be deleted. The post identifier is specified in the SocialPost.Id property
        """
        return_type = ClientResult(self.context, SocialThread())
        payload = {"postId": post_id}
        qry = ServiceOperationQuery(self, "DeletePost", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def create_file_attachment(self, name, description, file_data):
        """Creates a file attachment for a future post.

        Args:
            name (str): The name of the file.
            description (str): An optional description of the file.
            file_data (str or bytes): A stream for reading the file data.
        """
        return_type = ClientResult(self.context, SocialAttachment())
        payload = {"name": name, "description": description, "fileData": file_data}
        qry = ServiceOperationQuery(self, "CreateFileAttachment", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def get_feed(self, feed_type=None, options=None):
        """The GetFeed method returns a feed for the current user. The feed consists of an array of message threads.
        Each thread consists of a root post and an array of reply posts. See section 3.1.5.17 for details on
        the SocialFeed type. The server selects a set of posts to return in the feed based on the type
        and options parameters, but this protocol does require any specific algorithm to select the set of posts
        from all posts that meet the specified type and options.

        Args:
            feed_type (int): Specifies the type of feed to be returned. Feeds can be viewed using a personal view, news view, timeline view, or likes view. If the type is not specified, GetFeed returns the news view.
            options (SocialFeedOptions): Specifies the maximum number of threads to get in the feed, the sort order of the threads, and how the threads are to be selected based on the date and time that the threads were created.
        """
        return_type = ClientResult(self.context, SocialFeed())
        payload = {"type": feed_type, "options": options}
        qry = ServiceOperationQuery(self, "GetFeed", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def owner(self) -> SocialActor:
        """The Owner property returns the current user."""
        return self.properties.get("Owner", SocialActor())

    @property
    def personal_site_portal_uri(self) -> Optional[str]:
        """The PersonalSitePortalUri property specifies the URI of the personal site portal."""
        return self.properties.get("PersonalSitePortalUri", None)

    @property
    def entity_type_name(self):
        return "SP.Social.SocialFeedManager"
