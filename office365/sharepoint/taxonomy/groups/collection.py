from __future__ import annotations

from office365.runtime.client_runtime_context import ClientRuntimeContext
from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.taxonomy.groups.group import TermGroup
from office365.sharepoint.taxonomy.item_collection import TaxonomyItemCollection


class TermGroupCollection(TaxonomyItemCollection[TermGroup]):
    """A collection of TermGroup (section 3.1.5.18) objects"""

    def __init__(self, context: ClientRuntimeContext, resource_path: ResourcePath | None = None):
        super().__init__(context, TermGroup, resource_path)

    def get_by_name(self, name: str) -> TermGroup:
        """Returns the term group with the specified name.

        Args:
            name (str): The name of the TermGroup.
        """
        return self.single(f"name eq '{name}'")
