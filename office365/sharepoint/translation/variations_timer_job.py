from __future__ import annotations

from typing import List

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.entity import Entity


class VariationsTranslationTimerJob(Entity):
    """The VariationsTranslationTimerJob type provides methods to drive translation
    for list items in a variation label."""

    @staticmethod
    def export_items(
        context: ClientContext,
        list_url: str,
        item_ids: List[int],
        addresses_to_email: List[str] | None = None,
    ) -> VariationsTranslationTimerJob:
        """Exports a specific set of list items.

        Args:
            context: The SharePoint client context.
            list_url: Server-relative URL for the list containing the list items.
            item_ids: Identifiers of the list items to be exported.
            addresses_to_email: Email addresses to notify when the operation completes.
        """
        payload = {
            "list": list_url,
            "itemIds": item_ids,
            "addressesToEmail": addresses_to_email,
        }
        binding_type = VariationsTranslationTimerJob(context)
        qry = ServiceOperationQuery(binding_type, "ExportItems", None, payload, is_static=True)
        context.add_query(qry)
        return binding_type

    @property
    def entity_type_name(self) -> str:
        return "SP.Translation.VariationsTranslationTimerJob"
