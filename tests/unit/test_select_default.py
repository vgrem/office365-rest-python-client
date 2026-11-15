"""What a read asks for is declared by the type, one member at a time.

A caller with no opinion about columns gets the ones the type ranks (``@odata(default=..)``),
so the selection is stated where the member is stated. Two things follow and are pinned here:
the rank decides the order, not the class body, and a type that ranks nothing adds no
projection at all -- an empty answer is a decision, not a gap to be filled with a guess.
"""

from typing import Optional

from office365.migration.offline import offline_context
from office365.runtime.client_object import ClientObject
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.schema import TypeSchema
from office365.runtime.types.odata_property import odata


class Widget(ClientObject):
    #: Declared first, ranked second: the class body's order is how the CSDL lists the
    #: columns, and a table leads with a name rather than with a timestamp.
    @odata(name="createdDateTime", default=2)
    @property
    def created_at(self) -> Optional[str]:
        return self.properties.get("createdDateTime", None)

    @odata(name="title", default=1)
    @property
    def title(self) -> Optional[str]:
        return self.properties.get("title", None)

    @odata(name="eTag")
    @property
    def e_tag(self) -> Optional[str]:
        return self.properties.get("eTag", None)

    @odata(name="parent", navigation=True, default=3)
    @property
    def parent(self) -> Optional["Widget"]:
        return Widget(self.context)


class Gadget(Widget):
    """Ranking a member once is enough: a subclass reads its base's columns."""


class Plain(ClientObject):
    @odata(name="config")
    @property
    def config(self) -> Optional[str]:
        return self.properties.get("config", None)


def test_a_read_asks_for_the_ranked_columns_in_rank_order():
    widget = Widget(offline_context()).select_default()
    assert widget.query_options.select == ["title", "createdDateTime"]


def test_a_link_is_not_a_column_even_when_the_type_ranks_it():
    assert TypeSchema.of(Widget).defaults == ("title", "createdDateTime")


def test_a_type_that_ranks_nothing_adds_no_projection():
    assert Plain(offline_context()).select_default().query_options.select == []


def test_a_collection_asks_for_what_its_items_rank():
    collection = ClientObjectCollection(offline_context(), Widget, None)
    assert collection.select_default().query_options.select == ["title", "createdDateTime"]


def test_a_subclass_inherits_the_selection_its_base_states():
    assert TypeSchema.of(Gadget).defaults == TypeSchema.of(Widget).defaults
