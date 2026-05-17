from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class MicrofeedPostDefinition(ClientValue):
    def __init__(
        self,
        can_delete: Optional[bool] = None,
        can_follow_up: Optional[bool] = None,
        can_have_attachments: Optional[bool] = None,
        can_like: Optional[bool] = None,
        can_lock: Optional[bool] = None,
        can_reply: Optional[bool] = None,
        creation_time: Optional[datetime] = None,
        definition_id: Optional[int] = None,
        definition_name: Optional[str] = None,
        definition_version: Optional[int] = None,
        enable_people_list: Optional[bool] = None,
        is_default: Optional[bool] = None,
        is_enabled: Optional[bool] = None,
        is_notification: Optional[bool] = None,
        is_private: Optional[bool] = None,
        is_user_post: Optional[bool] = None,
        last_update_time: Optional[datetime] = None,
        partition_id: Optional[str] = None,
        persist_to_cache: Optional[bool] = None,
        persist_to_private_folder: Optional[bool] = None,
        persist_to_published_feed: Optional[bool] = None,
        reference_like_post_name: Optional[str] = None,
        reference_mention_post_name: Optional[str] = None,
        reference_reply_post_name: Optional[str] = None,
        render_post_author_image: Optional[bool] = None,
        resource_file_name: Optional[str] = None,
        security_trim_content_url: Optional[bool] = None,
        small_image_size_preferred: Optional[bool] = None,
    ):
        self.CanDelete = can_delete
        self.CanFollowUp = can_follow_up
        self.CanHaveAttachments = can_have_attachments
        self.CanLike = can_like
        self.CanLock = can_lock
        self.CanReply = can_reply
        self.CreationTime = creation_time
        self.DefinitionId = definition_id
        self.DefinitionName = definition_name
        self.DefinitionVersion = definition_version
        self.EnablePeopleList = enable_people_list
        self.IsDefault = is_default
        self.IsEnabled = is_enabled
        self.IsNotification = is_notification
        self.IsPrivate = is_private
        self.IsUserPost = is_user_post
        self.LastUpdateTime = last_update_time
        self.PartitionId = partition_id
        self.PersistToCache = persist_to_cache
        self.PersistToPrivateFolder = persist_to_private_folder
        self.PersistToPublishedFeed = persist_to_published_feed
        self.ReferenceLikePostName = reference_like_post_name
        self.ReferenceMentionPostName = reference_mention_post_name
        self.ReferenceReplyPostName = reference_reply_post_name
        self.RenderPostAuthorImage = render_post_author_image
        self.ResourceFileName = resource_file_name
        self.SecurityTrimContentUrl = security_trim_content_url
        self.SmallImageSizePreferred = small_image_size_preferred

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedPostDefinition"
