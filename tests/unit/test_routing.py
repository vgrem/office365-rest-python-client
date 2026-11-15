"""A route exists before a token does, because it is read from the annotations.

The router walks getters, so the two ways a generated getter says "this, or nothing" have to
be the same edge: a route the model already draws is not allowed to disappear because the
declaration was spelled ``Optional[X]``.
"""

from typing import Optional

from office365.routing import _links, chain, products
from office365.runtime.client_object import ClientObject


class Widget(ClientObject):
    pass


class Cabinet(ClientObject):
    @property
    def widget(self) -> Optional[Widget]:
        return Widget(self.context)

    @property
    def spare(self) -> "Widget | None":
        return None


def test_a_getter_that_may_return_nothing_is_a_link():
    links = _links(Cabinet)
    assert links["widget"] is Widget
    assert links["spare"] is Widget


def test_the_walk_reaches_the_widget_without_a_session():
    assert chain(Cabinet, Widget) == ("widget",)


def test_a_product_is_a_package_that_does_not_say_it_is_not_one():
    published = products()
    assert "directory" in published
    assert "runtime" not in published
