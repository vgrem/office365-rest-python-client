from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.admin.message_tracing_root import MessageTracingRoot
    from office365.common.mailbox import Mailbox


class ExchangeAdmin(Entity):
    @odata(name="mailboxes", navigation=True)
    @property
    def mailboxes(self) -> EntityCollection[Mailbox]:
        """Gets the mailboxes property"""
        from office365.common.mailbox import Mailbox

        return self.properties.get(
            "mailboxes", EntityCollection[Mailbox](self.context, Mailbox, ResourcePath("mailboxes", self.resource_path))
        )

    @odata(name="tracing", navigation=True)
    @property
    def tracing(self) -> MessageTracingRoot:
        """Gets the tracing property"""
        from office365.admin.message_tracing_root import MessageTracingRoot

        return self.properties.get(
            "tracing", MessageTracingRoot(self.context, ResourcePath("tracing", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ExchangeAdmin"
