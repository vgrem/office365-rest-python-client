from __future__ import annotations

from typing import TYPE_CHECKING

from office365.directory.permissions.require_permission import require_permission
from office365.entity_collection import EntityCollection
from office365.onedrive.termstore.sets.name import LocalizedName
from office365.onedrive.termstore.sets.set import Set
from office365.runtime.client_request_exception import ClientRequestException, DuplicatedObjectException
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.create_entity import CreateEntityQuery

if TYPE_CHECKING:
    from office365.onedrive.termstore.groups.group import Group


class SetCollection(EntityCollection[Set]):
    def __init__(self, context, resource_path=None, parent_group=None):
        """
        :param office365.onedrive.termstore.groups.group.Group parent_group: The parent group that contains the set
        """
        super().__init__(context, Set, resource_path)
        self._parent_group = parent_group

    @require_permission(
        delegated=["TermStore.Read.All", "TermStore.ReadWrite.All"],
        application=["TermStore.Read.All", "TermStore.ReadWrite.All"],
        notes="Get term set by name",
    )
    def get_by_name(self, name: str) -> Set:
        """Returns the TermSet specified by its name."""
        return_type = Set(self.context)
        self.add_child(return_type)

        def _after_loaded(sets: SetCollection):
            for s in sets:
                if s.display_name == name:
                    return_type.copy_from(s)
                    return

        self.get().after_execute(_after_loaded)

        return return_type

    @require_permission(
        delegated=["TermStore.ReadWrite.All"],
        application=["TermStore.ReadWrite.All"],
        notes="Create a new term set",
    )
    def add(self, name: str, parent_group: Group | None = None) -> Set:
        """Create a new set object.

        :param office365.onedrive.termstore.group.Group parent_group: The parent group that contains the set.
        :param str name: Default name (in en-US localization).
        """
        return_type = Set(self.context)
        self.add_child(return_type)

        if self._parent_group is not None:
            props = {"localizedNames": ClientValueCollection(LocalizedName, [LocalizedName(name)])}
            qry = CreateEntityQuery(self, props, return_type)
            self.context.add_query(qry)
        elif parent_group is not None:
            props = {
                "parentGroup": {"id": parent_group.get_property("id")},
                "localizedNames": ClientValueCollection(LocalizedName, [LocalizedName(name)]),
            }
            qry = CreateEntityQuery(self, props, return_type)
            self.context.add_query(qry)
        else:
            raise TypeError("Parameter 'parent_group' is not set")

        return return_type

    def get_or_add(self, name: str) -> Set:
        """Gets existing set by name or creates a new one (idempotent)."""
        term_set = self.add(name)

        def _on_name_exists(error: ClientRequestException):
            if not isinstance(error, DuplicatedObjectException):
                raise error

            def _load_existing(existing: Set):
                if existing.get_property("id") is not None:
                    term_set.copy_from(existing)
                else:
                    self.add(name).after_execute(lambda s: term_set.copy_from(s))

            self.get_by_name(name).after_execute(_load_existing)

        term_set.on_error(_on_name_exists)
        return term_set
