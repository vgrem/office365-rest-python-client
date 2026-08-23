from __future__ import annotations

from typing import TYPE_CHECKING

from office365.onedrive.termstore.groups.collection import GroupCollection
from office365.onedrive.termstore.sets.collection import SetCollection
from office365.onedrive.termstore.terms.collection import TermCollection

if TYPE_CHECKING:
    from office365.onedrive.termstore.store import Store


class StoreManager:
    """Traverse, search, and import the term store hierarchy.

    All operations are deferred: queries are queued and run with a single
    ``execute_query()``. ``get_all_terms()`` returns a flattened ``TermCollection``
    with each term's ``children`` attached, so the standard collection pipeline
    (``to_json()``, ``write_csv``) can serialize the full tree.
    """

    def __init__(self, store: Store):
        self.store = store

    def get_all_terms(self) -> TermCollection:
        """Flatten the whole term store into a single ``TermCollection``.

        Traverses groups -> sets -> terms -> children and collects every term
        into one flat collection. No queries run until ``execute_query()``.
        """
        all_terms = TermCollection(self.store.context)

        def _on_terms_loaded(terms: TermCollection) -> None:
            for term in terms:
                all_terms.add_child(term)
                term.children.get().after_execute(_on_terms_loaded)

        def _on_sets_loaded(sets: SetCollection) -> None:
            for term_set in sets:
                term_set.children.get().after_execute(_on_terms_loaded)

        def _on_groups_loaded(groups: GroupCollection) -> None:
            for group in groups:
                group.sets.get().after_execute(_on_sets_loaded)

        self.store.groups.get().after_execute(_on_groups_loaded)
        return all_terms

    def search_term(self, search_label: str) -> TermCollection:
        """Search for a term by label across all sets in the term store."""
        return_type = TermCollection(self.store.context)

        def _on_terms_loaded(terms: TermCollection) -> None:
            for t in terms:
                if t.display_name == search_label:
                    return_type.add_child(t)

        def _on_sets_loaded(sets: SetCollection) -> None:
            for s in sets:
                s.terms.get().after_execute(lambda terms: _on_terms_loaded(terms))

        def _on_groups_loaded(groups: GroupCollection) -> None:
            for g in groups:
                g.sets.get().after_execute(lambda sets: _on_sets_loaded(sets))

        self.store.groups.get().after_execute(lambda groups: _on_groups_loaded(groups))
        return return_type

    def from_json(self, data: list[dict]) -> Store:
        """Import a term hierarchy from a list of group dicts.

        Args:
            data: List of ``{name, sets: [{name, children: [{name, children: []}]}]}``.

        Returns:
            self.store for chaining — call ``execute_query()`` to process.
        """
        for group_data in data:
            group = self.store.ensure_group(group_data["name"])
            for set_data in group_data.get("sets", []):
                term_set = group.ensure_set(set_data["name"])
                self._create_terms(term_set.children, set_data.get("children", []))
        return self.store

    def _create_terms(self, collection: TermCollection, terms: list[dict]) -> None:
        for term_data in terms:
            node = collection.ensure(term_data["name"])
            self._create_terms(node.children, term_data.get("children", []))
