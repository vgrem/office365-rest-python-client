from __future__ import annotations

from typing import TYPE_CHECKING

from office365.onedrive.termstore.terms.collection import TermCollection

if TYPE_CHECKING:
    from office365.onedrive.termstore.store import Store


class StoreImporter:
    def __init__(self, store: Store):
        self.store = store

    def import_from_data(self, data: list[dict]) -> Store:
        """Import term hierarchy from a parsed JSON list.

        Args:
            data: List of group dicts matching the export format.

        Returns:
            self.store for chaining — call .context.execute_query() to process.
        """
        for group_data in data:
            group = self.store.groups.get_or_add(group_data["name"])
            for set_data in group_data.get("sets", []):
                term_set = group.sets.get_or_add(set_data["name"])
                self._import_terms(term_set.children, set_data.get("children", []))
        return self.store

    def _import_terms(self, collection: TermCollection, terms: list[dict]):
        for t in terms:
            node = collection.get_or_add(t["name"])
            self._import_terms(node.children, t.get("children", []))
