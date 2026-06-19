from __future__ import annotations

from typing import TYPE_CHECKING

from office365.onedrive.termstore.sets.collection import SetCollection
from office365.onedrive.termstore.terms.collection import TermCollection
from office365.runtime.client_result import ClientResult

if TYPE_CHECKING:
    from office365.onedrive.termstore.groups.collection import GroupCollection
    from office365.onedrive.termstore.store import Store


class StoreExporter:
    def __init__(self, store: Store):
        self.store = store

    def export(self) -> ClientResult[list[dict]]:
        return_type = ClientResult(self.store.context, [])

        def _on_groups_loaded(groups: GroupCollection):
            for g in groups:
                gd = {"name": g.display_name, "sets": []}
                return_type.value.append(gd)
                g.sets.get().after_execute(lambda sets, gd=gd: _on_sets_loaded(sets, gd))

        def _on_sets_loaded(sets: SetCollection, group_data: dict):
            for s in sets:
                sd = {"name": s.display_name, "children": []}
                group_data["sets"].append(sd)
                s.children.get().after_execute(lambda terms, sd=sd: _on_terms_loaded(terms, sd))

        def _on_terms_loaded(terms: TermCollection, parent_item: dict):
            for term in terms:
                child = {"name": term.display_name}
                parent_item.setdefault("children", []).append(child)
                term.children.get().after_execute(lambda t, c=child: _on_terms_loaded(t, c))

        self.store.groups.get().after_execute(_on_groups_loaded)
        return return_type
