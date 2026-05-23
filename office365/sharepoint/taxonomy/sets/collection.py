from __future__ import annotations

from office365.runtime.client_runtime_context import ClientRuntimeContext
from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.taxonomy.item_collection import TaxonomyItemCollection
from office365.sharepoint.taxonomy.sets.set import TermSet


class TermSetCollection(TaxonomyItemCollection[TermSet]):
    def __init__(self, context: ClientRuntimeContext, resource_path: ResourcePath | None = None):
        super().__init__(context, TermSet, resource_path)
