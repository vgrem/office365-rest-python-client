from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, List, Optional

from office365.communications.callrecords.collection import CallRecordCollection
from office365.communications.calls.collection import CallCollection
from office365.communications.onlinemeetings.collection import OnlineMeetingCollection
from office365.communications.presences.presence import Presence
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.permissions import require_permission
from office365.runtime.odata.literals import odata_literal
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.communications.adhoc_call import AdhocCall
    from office365.communications.onlinemeetings.engagement_conversation import (
        OnlineMeetingEngagementConversation,
    )
    from office365.teams.viva.engagement.conversation_message import EngagementConversationMessage


class CloudCommunications(Entity):
    """ """

    @require_permission(delegated=["Presence.Read.All"], application=["Presence.Read.All"])
    def get_presences_by_user_id(
        self, ids: List[str], return_type: Optional[EntityCollection[Presence]] = None
    ) -> EntityCollection[Presence]:
        """Get the presence information for multiple users.

        Args:
            ids (list[str]): The user object IDs.
            return_type (EntityCollection[Presence]): The collection to read the
                answer into, when the caller already holds one; see
                :meth:`get_presences_by_principal_name`.
        """
        if return_type is None:
            return_type = EntityCollection(self.context, Presence, ResourcePath("presences", self.resource_path))
        qry = ServiceOperationQuery(self, "getPresencesByUserId", None, {"ids": ids}, None, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=["Presence.Read.All", "User.Read.All"],
        application=["Presence.Read.All", "User.Read.All"],
        notes="the second scope is the directory read behind each name",
    )
    def get_presences_by_principal_name(self, users: Iterable[str]) -> EntityCollection[Presence]:
        """The presence of people named by user principal name.

        ``getPresencesByUserId`` takes object ids: handed a principal name it
        answers ``PresenceUnknown`` for that person instead of an error, which
        reads as "they are offline". So the names are read from the directory
        first, and when that read answers its ids go to
        :meth:`get_presences_by_user_id`. The action joins the same queue, behind
        the read, so one ``execute_query()`` runs both:

        >>> presences = client.communications.get_presences_by_principal_name(upns)
        >>> presences.execute_query()

        The read is one ``$filter`` over ``userPrincipalName``, so it names at
        most 15 people (a wider ``or`` chain is rejected by the service), and a
        name the tenant does not have matches nothing and is simply absent from
        the answer. The action answers at most 650 ids per request, and its rows
        are keyed by object id — the response order is not guaranteed, so pair
        the addresses you asked for with the ids separately when you need the
        addresses back.
        """
        names = list(dict.fromkeys(users))
        presences = EntityCollection(self.context, Presence, ResourcePath("presences", self.resource_path))
        if not names:
            return presences
        condition = " or ".join(f"userPrincipalName eq {odata_literal(name)}" for name in names)
        resolved = self.context.users.filter(condition).get_all()
        resolved.after_execute(
            lambda found: self.get_presences_by_user_id([user.id for user in found if user.id], presences)
        )
        return presences

    @odata(name="calls", navigation=True)
    @property
    def calls(self) -> CallCollection:
        """ " """
        return self.properties.get("calls", CallCollection(self.context, ResourcePath("calls", self.resource_path)))

    @odata(name="callRecords", navigation=True)
    @property
    def call_records(self) -> CallRecordCollection:
        """ " """
        return self.properties.get(
            "callRecords", CallRecordCollection(self.context, ResourcePath("callRecords", self.resource_path))
        )

    @odata(name="onlineMeetings", navigation=True)
    @property
    def online_meetings(self) -> OnlineMeetingCollection:
        """ " """
        return self.properties.get(
            "onlineMeetings", OnlineMeetingCollection(self.context, ResourcePath("onlineMeetings", self.resource_path))
        )

    @odata(name="presences", navigation=True)
    @property
    def presences(self) -> EntityCollection[Presence]:
        """ " """
        return self.properties.get(
            "presences", EntityCollection(self.context, Presence, ResourcePath("presences", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudCommunications"

    @odata(name="adhocCalls", navigation=True)
    @property
    def adhoc_calls(self) -> EntityCollection[AdhocCall]:
        """Gets the adhocCalls property"""
        from office365.communications.adhoc_call import AdhocCall

        return self.properties.get(
            "adhocCalls",
            EntityCollection[AdhocCall](self.context, AdhocCall, ResourcePath("adhocCalls", self.resource_path)),
        )

    @odata(name="onlineMeetingConversations", navigation=True)
    @property
    def online_meeting_conversations(self) -> EntityCollection[OnlineMeetingEngagementConversation]:
        """Gets the onlineMeetingConversations property"""
        from office365.communications.onlinemeetings.engagement_conversation import (
            OnlineMeetingEngagementConversation,
        )

        return self.properties.get(
            "onlineMeetingConversations",
            EntityCollection[OnlineMeetingEngagementConversation](
                self.context,
                OnlineMeetingEngagementConversation,
                ResourcePath("onlineMeetingConversations", self.resource_path),
            ),
        )

    def get_all_online_meeting_messages(self) -> EntityCollection[EngagementConversationMessage]:
        """getAllOnlineMeetingMessages operation."""
        from office365.teams.viva.engagement.conversation_message import EngagementConversationMessage

        return_type = EntityCollection(self.context, EngagementConversationMessage)
        qry = FunctionQuery(self, "getAllOnlineMeetingMessages", None, return_type)
        self.context.add_query(qry)
        return return_type
