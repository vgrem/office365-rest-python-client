from typing import TYPE_CHECKING, List

from typing_extensions import Self

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.recyclebin.item import RecycleBinItem

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class RecycleBinItemCollection(EntityCollection[RecycleBinItem]):
    """Represents a collection of View resources."""

    def __init__(self, context: "ClientContext", resource_path: ResourcePath = None):
        super(RecycleBinItemCollection, self).__init__(
            context, RecycleBinItem, resource_path
        )

    def delete_all_second_stage_items(self) -> Self:
        """Permanently deletes all Recycle Bin items in the second-stage Recycle Bin"""
        qry = ServiceOperationQuery(self, "DeleteAllSecondStageItems")
        self.context.add_query(qry)
        return self

    def delete_by_ids(self, ids: List[str]) -> Self:
        """
        Permanently deletes Recycle Bin items by their identifiers

        :param list[str] ids: Recycle Bin items identifiers
        """
        payload = {"ids": StringCollection(ids)}
        qry = ServiceOperationQuery(self, "DeleteByIds", None, payload)
        self.context.add_query(qry)
        return self

    def move_to_second_stage_by_ids(self, ids: List[str]) -> Self:
        """
        Moves all Recycle Bin items from the first-stage Recycle Bin to the second-stage Recycle Bin by their identifies

        :param list[str] ids: Recycle Bin items identifiers
        """
        payload = {"ids": StringCollection(ids)}
        qry = ServiceOperationQuery(self, "MoveToSecondStageByIds", None, payload)
        self.context.add_query(qry)
        return self

    def move_all_to_second_stage(self) -> Self:
        """
        Moves all Recycle Bin items from the first-stage Recycle Bin to the second-stage Recycle Bin if the
        SecondStageRecycleBinQuota property of the current web application is not 0.
        Otherwise, permanently deletes all Recycle Bin items.
        """
        qry = ServiceOperationQuery(self, "MoveAllToSecondStage")
        self.context.add_query(qry)
        return self

    def get_by_id(self, recycle_bin_id: str) -> RecycleBinItem:
        """
        Returns the recycle bin type with the given identifier from the collection.

        :param str recycle_bin_id: A hexadecimal value representing the identifier of a recycle bin.
        """
        return RecycleBinItem(
            self.context,
            ServiceOperationPath("GetById", [recycle_bin_id], self.resource_path),
        )

    def delete_all(self) -> Self:
        """Permanently deletes all Recycle Bin items."""
        qry = ServiceOperationQuery(self, "DeleteAll")
        self.context.add_query(qry)
        return self

    def restore_all(self) -> Self:
        """Restores all Recycle Bin items to their original locations."""
        qry = ServiceOperationQuery(self, "RestoreAll")
        self.context.add_query(qry)
        return self
