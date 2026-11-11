"""A type's identity is declared once, above the class, and read in one place.

``TypeSchema.key`` is the value: it decides which value re-anchors an entity's path and
which name a read forces into ``$select``. What was missing was one owner for the answer
-- so it was written by hand, per class, 21 times. ``@key(...)`` is that owner, and these
tests pin the three things that make it a drop-in: a type that declares nothing is
addressed the way its family is, a declaration reaches both readers, and a key one path
segment cannot hold is refused instead of mis-addressed.
"""

from __future__ import annotations

from typing import Optional

import pytest
from office365.entity import Entity
from office365.graph_client import GraphClient
from office365.runtime.types.odata_property import CompositeKeyNotSupported, key, odata
from office365.sharepoint.entity import Entity as SharePointEntity


@key("tenantId")
class _Partner(Entity):
    @odata(name="tenantId")
    @property
    def tenant_id(self) -> Optional[str]:
        return self.properties.get("tenantId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Partner"


class _Inheriting(_Partner):
    """A derived type inherits the key, exactly as it inherits the declared property."""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.InheritingPartner"


def test_a_type_with_no_declaration_answers_its_family_default():
    class _Plain(Entity):
        @property
        def entity_type_name(self) -> str:
            return "microsoft.graph.Plain"

    assert _Plain._schema.key == "id"


def test_sharepoint_keeps_its_own_default():
    class _PlainItem(SharePointEntity):
        @property
        def entity_type_name(self) -> str:
            return "SP.PlainItem"

    assert _PlainItem._schema.key == "Id"


def test_a_declared_key_reaches_the_reader():
    """The decorator sits above a class whose schema was built already, so it rebuilds it."""
    assert _Partner._schema.key == "tenantId"
    assert _Partner(GraphClient())._schema.key == "tenantId"


def test_a_declared_key_is_inherited():
    assert _Inheriting._schema.key == "tenantId"
    assert _Inheriting(GraphClient())._schema.key == "tenantId"


def test_the_declared_key_re_anchors_the_path():
    """What ``set_property`` asks: only the key re-anchors, and only its own name."""
    entity = _Partner(GraphClient())

    entity.set_property("tenantId", "contoso")
    assert str(entity.resource_path) == "/contoso"


def test_the_default_key_still_re_anchors_a_plain_entity():
    entity = Entity(GraphClient())

    entity.set_property("id", "123")
    assert str(entity.resource_path) == "/123"


def test_a_read_widens_select_with_the_declared_key():
    """What ``ensure_properties`` asks: the identity is fetched, so the path can be rebuilt."""
    client = GraphClient()
    entity = _Partner(client)

    entity.ensure_properties(["displayName"])

    assert client._queries[-1].query_options.select == ["displayName", "tenantId"]


def test_a_read_on_a_plain_entity_still_widens_select_with_id():
    client = GraphClient()
    entity = Entity(client)

    entity.ensure_properties(["displayName"])

    assert client._queries[-1].query_options.select == ["displayName", "id"]


def test_an_undeclared_key_re_anchors_nothing():
    """Setting ``id`` on a type whose identity is ``tenantId`` must not move the path."""
    entity = _Partner(GraphClient())

    entity.set_property("id", "123")

    assert entity.resource_path is None


def test_a_composite_key_is_refused_rather_than_half_supported():
    with pytest.raises(CompositeKeyNotSupported, match="appId/tenantId"):

        @key("appId", "tenantId")
        class _Composite(Entity):
            pass


def test_a_key_naming_nothing_clears_the_inherited_one():
    """A folder is reached by its path, so an ``Id`` it is handed must not re-anchor it."""

    @key()
    class _Unkeyed(SharePointEntity):
        @property
        def entity_type_name(self) -> str:
            return "SP.Folder"

    assert _Unkeyed._schema.key == ""
    entity = _Unkeyed(GraphClient())
    entity.set_property("Id", "7e1c")
    assert entity.resource_path is None
