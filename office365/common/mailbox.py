from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.common.mailbox_folder import MailboxFolder
    from office365.outlook.mail.export_item_response import ExportItemResponse
    from office365.outlook.mail.mailbox_item_import_session import MailboxItemImportSession


class Mailbox(Entity):
    @odata(name="folders", navigation=True)
    @property
    def folders(self) -> EntityCollection[MailboxFolder]:
        """Gets the folders property"""
        from office365.common.mailbox_folder import MailboxFolder

        return self.properties.get(
            "folders",
            EntityCollection[MailboxFolder](self.context, MailboxFolder, ResourcePath("folders", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Mailbox"

    def create_import_session(self) -> ClientResult[MailboxItemImportSession]:
        """createImportSession operation."""
        from office365.outlook.mail.mailbox_item_import_session import MailboxItemImportSession

        return_type = ClientResult(self.context, MailboxItemImportSession())
        qry = ServiceOperationQuery(self, "createImportSession", None, {}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def export_items(self, item_ids: list[str]) -> ClientResult[ClientValueCollection[ExportItemResponse]]:
        """exportItems operation.

        Args:
            item_ids (list[str]):
                ItemIds parameter
        """
        from office365.outlook.mail.export_item_response import ExportItemResponse

        return_type = ClientResult(self.context, ClientValueCollection(ExportItemResponse))
        qry = ServiceOperationQuery(
            self, "exportItems", None, {"ItemIds": StringCollection(item_ids)}, None, return_type
        )
        self.context.add_query(qry)
        return return_type
