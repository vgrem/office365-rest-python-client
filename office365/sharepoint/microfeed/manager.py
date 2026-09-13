from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.v3.static import StaticPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.microfeed.entity import MicroBlogEntity
from office365.sharepoint.microfeed.posts.options import MicrofeedPostOptions
from office365.sharepoint.microfeed.retrievaloptions import MicrofeedRetrievalOptions
from office365.sharepoint.social.microfeed.thread import MicrofeedThread
from office365.sharepoint.social.microfeed.thread_collection import MicrofeedThreadCollection


class MicrofeedManager(Entity):
    @property
    def resource_path(self):
        if self._resource_path is None:
            self._resource_path = StaticPath("SP.Microfeed.MicrofeedManager")
        return self._resource_path

    @property
    def current_user(self) -> MicroBlogEntity:
        """Gets the CurrentUser property"""
        return self.properties.get("CurrentUser", MicroBlogEntity())

    @property
    def is_feed_activity_public(self) -> Optional[bool]:
        """Gets the IsFeedActivityPublic property"""
        return self.properties.get("IsFeedActivityPublic", None)

    @property
    def static_thread_link(self) -> Optional[str]:
        """Gets the StaticThreadLink property"""
        return self.properties.get("StaticThreadLink", None)

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedManager"

    def add_user_to_post_people_list(self, post_identifier: str, user_login_name: str) -> ClientResult[int]:
        """AddUserToPostPeopleList operation.

        Args:
            post_identifier (str): postIdentifier parameter
            user_login_name (str): UserLoginName parameter
        """
        return_type = ClientResult(self.context, int())
        qry = ServiceOperationQuery(
            self,
            "AddUserToPostPeopleList",
            None,
            {"postIdentifier": post_identifier, "UserLoginName": user_login_name},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def clear_unread_mentions_count(self) -> ClientResult[int]:
        """ClearUnreadMentionsCount operation."""
        return_type = ClientResult(self.context, int())
        qry = ServiceOperationQuery(self, "ClearUnreadMentionsCount", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def delete_by_id(self, post_identifier: str) -> ClientResult[MicrofeedThread]:
        """DeleteById operation.

        Args:
            post_identifier (str): postIdentifier parameter
        """
        return_type = ClientResult(self.context, MicrofeedThread())
        qry = ServiceOperationQuery(self, "DeleteById", None, {"postIdentifier": post_identifier}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def delete_user_from_post_people_list(self, post_identifier: str, user_login_name: str) -> ClientResult[int]:
        """DeleteUserFromPostPeopleList operation.

        Args:
            post_identifier (str): postIdentifier parameter
            user_login_name (str): UserLoginName parameter
        """
        return_type = ClientResult(self.context, int())
        qry = ServiceOperationQuery(
            self,
            "DeleteUserFromPostPeopleList",
            None,
            {"postIdentifier": post_identifier, "UserLoginName": user_login_name},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def get_my_categorical_feed(
        self, feed_options: MicrofeedRetrievalOptions
    ) -> ClientResult[MicrofeedThreadCollection]:
        """GetMyCategoricalFeed operation.

        Args:
            feed_options (MicrofeedRetrievalOptions): feedOptions parameter
        """
        return_type = ClientResult(self.context, MicrofeedThreadCollection())
        qry = ServiceOperationQuery(self, "GetMyCategoricalFeed", None, {"feedOptions": feed_options}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def get_my_consolidated_feed(
        self, feed_options: MicrofeedRetrievalOptions
    ) -> ClientResult[MicrofeedThreadCollection]:
        """GetMyConsolidatedFeed operation.

        Args:
            feed_options (MicrofeedRetrievalOptions): feedOptions parameter
        """
        return_type = ClientResult(self.context, MicrofeedThreadCollection())
        qry = ServiceOperationQuery(
            self, "GetMyConsolidatedFeed", None, {"feedOptions": feed_options}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def get_my_published_feed(
        self, feed_options: MicrofeedRetrievalOptions, type_of_pub_feed: int, show_public_view: bool
    ) -> ClientResult[MicrofeedThreadCollection]:
        """GetMyPublishedFeed operation.

        Args:
            feed_options (MicrofeedRetrievalOptions): feedOptions parameter
            type_of_pub_feed (int): typeOfPubFeed parameter
            show_public_view (bool): ShowPublicView parameter
        """
        return_type = ClientResult(self.context, MicrofeedThreadCollection())
        qry = ServiceOperationQuery(
            self,
            "GetMyPublishedFeed",
            None,
            {"feedOptions": feed_options, "typeOfPubFeed": type_of_pub_feed, "ShowPublicView": show_public_view},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def get_published_feed(
        self, feed_owner: str, feed_options: MicrofeedRetrievalOptions, type_of_pub_feed: int
    ) -> ClientResult[MicrofeedThreadCollection]:
        """GetPublishedFeed operation.

        Args:
            feed_owner (str): feedOwner parameter
            feed_options (MicrofeedRetrievalOptions): feedOptions parameter
            type_of_pub_feed (int): typeOfPubFeed parameter
        """
        return_type = ClientResult(self.context, MicrofeedThreadCollection())
        qry = ServiceOperationQuery(
            self,
            "GetPublishedFeed",
            None,
            {"feedOwner": feed_owner, "feedOptions": feed_options, "typeOfPubFeed": type_of_pub_feed},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def get_thread(self, post_identifier: str) -> ClientResult[MicrofeedThread]:
        """GetThread operation.

        Args:
            post_identifier (str): postIdentifier parameter
        """
        return_type = ClientResult(self.context, MicrofeedThread())
        qry = ServiceOperationQuery(self, "GetThread", None, {"postIdentifier": post_identifier}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def get_unread_mentions_count(self) -> ClientResult[int]:
        """GetUnreadMentionsCount operation."""
        return_type = ClientResult(self.context, int())
        qry = ServiceOperationQuery(self, "GetUnreadMentionsCount", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def like(self, post_identifier: str) -> ClientResult[MicrofeedThread]:
        """Like operation.

        Args:
            post_identifier (str): postIdentifier parameter
        """
        return_type = ClientResult(self.context, MicrofeedThread())
        qry = ServiceOperationQuery(self, "Like", None, {"postIdentifier": post_identifier}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def lock_thread_by_id(self, thread_identifier: str) -> ClientResult[MicrofeedThread]:
        """LockThreadById operation.

        Args:
            thread_identifier (str): threadIdentifier parameter
        """
        return_type = ClientResult(self.context, MicrofeedThread())
        qry = ServiceOperationQuery(
            self, "LockThreadById", None, {"threadIdentifier": thread_identifier}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def post(self, post_options: MicrofeedPostOptions) -> ClientResult[MicrofeedThread]:
        """Post operation.

        Args:
            post_options (MicrofeedPostOptions): postOptions parameter
        """
        return_type = ClientResult(self.context, MicrofeedThread())
        qry = ServiceOperationQuery(self, "Post", None, {"postOptions": post_options}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def post_reply(
        self, post_identifier: str, post_reply_options: MicrofeedPostOptions
    ) -> ClientResult[MicrofeedThread]:
        """PostReply operation.

        Args:
            post_identifier (str): postIdentifier parameter
            post_reply_options (MicrofeedPostOptions): postReplyOptions parameter
        """
        return_type = ClientResult(self.context, MicrofeedThread())
        qry = ServiceOperationQuery(
            self,
            "PostReply",
            None,
            {"postIdentifier": post_identifier, "postReplyOptions": post_reply_options},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    def repopulate_lmt(self, time_stamp: datetime, secure_hash: str) -> ClientResult[int]:
        """RepopulateLMT operation.

        Args:
            time_stamp (datetime): timeStamp parameter
            secure_hash (str): secureHash parameter
        """
        return_type = ClientResult(self.context, int())
        qry = ServiceOperationQuery(
            self, "RepopulateLMT", None, {"timeStamp": time_stamp, "secureHash": secure_hash}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def un_like(self, post_identifier: str) -> ClientResult[MicrofeedThread]:
        """UnLike operation.

        Args:
            post_identifier (str): postIdentifier parameter
        """
        return_type = ClientResult(self.context, MicrofeedThread())
        qry = ServiceOperationQuery(self, "UnLike", None, {"postIdentifier": post_identifier}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def un_lock_thread_by_id(self, thread_identifier: str) -> ClientResult[MicrofeedThread]:
        """UnLockThreadById operation.

        Args:
            thread_identifier (str): threadIdentifier parameter
        """
        return_type = ClientResult(self.context, MicrofeedThread())
        qry = ServiceOperationQuery(
            self, "UnLockThreadById", None, {"threadIdentifier": thread_identifier}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def unsubscribe_from_e_mail(self, post_identifier: str) -> Self:
        """UnsubscribeFromEMail operation.

        Args:
            post_identifier (str): postIdentifier parameter
        """
        qry = ServiceOperationQuery(self, "UnsubscribeFromEMail", None, {"postIdentifier": post_identifier}, None, None)
        self.context.add_query(qry)
        return self
