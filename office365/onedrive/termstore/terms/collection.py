from __future__ import annotations

from office365.directory.permissions.require_permission import require_permission
from office365.entity_collection import EntityCollection
from office365.onedrive.termstore.terms.label import LocalizedLabel
from office365.onedrive.termstore.terms.term import Term
from office365.runtime.client_request_exception import ClientRequestException, DuplicatedObjectException
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.v4.entity import EntityPath
from office365.runtime.queries.create_entity import CreateEntityQuery


class TermCollection(EntityCollection[Term]):
    def __init__(self, context, resource_path=None, parent_term: Term | None = None):
        super().__init__(context, Term, resource_path)
        self._parent_term = parent_term

    @require_permission(
        delegated=["TermStore.ReadWrite.All"],
        application=["TermStore.ReadWrite.All"],
        notes="Create a new term in a term set",
    )
    def add(self, label: str) -> Term:
        """Create a new term object.

        :param str label: The name of the label.
        """
        return_type = Term(self.context, EntityPath(None, self.resource_path))
        self.add_child(return_type)

        props = {"labels": ClientValueCollection(LocalizedLabel, [LocalizedLabel(label)])}
        qry = CreateEntityQuery(self, props, return_type)
        self.context.add_query(qry)

        return return_type

    def get_by_label(self, label: str) -> Term:
        return_type = Term(self.context)
        self.add_child(return_type)

        def _after_loaded(terms: TermCollection):
            for t in terms:
                if t.display_name == label:
                    return_type.copy_from(t)
                    return

        self.get().after_execute(_after_loaded)

        return return_type

    def get_or_add(self, label: str) -> Term:
        term = self.add(label)

        def _on_name_exists(error: ClientRequestException):
            if not isinstance(error, DuplicatedObjectException):
                raise error

            def _load_existing(existing: Term):
                if existing.id is not None:
                    term.copy_from(existing)
                else:
                    self.add(label).after_execute(lambda t: term.copy_from(t))

            self.get_by_label(label).after_execute(_load_existing)

        term.on_error(_on_name_exists)
        return term
