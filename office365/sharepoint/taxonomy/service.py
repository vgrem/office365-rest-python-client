from __future__ import annotations

from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.taxonomy.stores.store import TermStore


class TaxonomyService(ClientContext):
    """Wraps all of the associated TermStore objects for an Site object."""

    def __init__(self, context: ClientContext):
        super().__init__(context.base_url)
        self._pending_request = context.pending_request()

    @property
    def service_root_url(self) -> str:
        """Get the API service root URL"""
        return f"{super().service_root_url}/v2.1"

    @property
    def term_store(self) -> TermStore:
        return TermStore(self, ResourcePath("termStore", None))
