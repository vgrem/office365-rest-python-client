"""Offline tests for Managed Metadata (taxonomy) field handling.

Covers the base-library fixes that make a taxonomy column usable: the field is
created without a ``List`` attribute (so its ``LookupList`` binds to the web's
hidden TaxonomyHiddenList), a multi-value collection is actually populated, and
a multi-value write lands on the hidden note companion column.

The term store export/import walk over the same managed-metadata types lives here
too — export reads a store tree, import replays it into queued creates.
"""

from __future__ import annotations

from office365.onedrive.termstore.store import Store
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.listitem import ListItem
from office365.sharepoint.taxonomy.create_xml_parameters import TaxonomyFieldCreateXmlParameters
from office365.sharepoint.taxonomy.field_value import TaxonomyFieldValue
from office365.sharepoint.taxonomy.field_value_col import TaxonomyFieldValueCollection
from tests import test_site_url
from tests._scripted_transport import ScriptedTransport


def _ctx(payloads):
    ctx = ClientContext(test_site_url)
    ctx.pending_request().beforeExecute.clear()
    ctx.pending_request().transport = ScriptedTransport(payloads)
    return ctx


def test_taxonomy_schema_omits_list_attribute():
    params = TaxonomyFieldCreateXmlParameters(
        Name="Dept",
        SspId="f02be691-d551-462f-aaae-e1c89168cd0b",
        TermSetId="4d7c4109-db97-4c49-8f7f-a72f0785ee3c",
        FieldId="11111111-1111-1111-1111-111111111111",
        WebId="22222222-2222-2222-2222-222222222222",
        TextFieldId="33333333-3333-3333-3333-333333333333",
    )
    schema = params.schema_xml
    assert 'Type="TaxonomyFieldType"' in schema
    assert "List=" not in schema
    assert 'WebId="22222222-2222-2222-2222-222222222222"' in schema
    assert "4d7c4109-db97-4c49-8f7f-a72f0785ee3c" in schema


def test_set_taxonomy_collection_writes_note_companion():
    note_id = "33333333-3333-3333-3333-333333333333"
    # The companion name is resolved synchronously (a deferred lookup would run
    # after the write payload was built): the taxonomy column's TextField id, then
    # the hidden note field, whose *item* property is its EntityPropertyName.
    ctx = _ctx(
        [
            {"d": {"TextField": note_id}},
            {"d": {"EntityPropertyName": "Dept_0"}},
        ]
    )
    lst = ctx.web.lists.get_by_title("Tasks")
    item = ListItem(ctx, None, lst)
    item.set_property("Dept", TaxonomyFieldValueCollection([TaxonomyFieldValue(Label="TermA", TermGuid="a" * 8)]))
    assert item.properties.get("Dept_0") == "-1;#TermA|aaaaaaaa"


# --- The term store: export reads a tree, import replays it ------------------------------------------------


class _FakeTerms:
    def __init__(self, items=None):
        self.items = list(items or [])

    def get(self):
        return self

    def after_execute(self, callback):
        callback(self.items)
        return self

    def ensure(self, name):
        node = _FakeTerm(name)
        self.items.append(node)
        return node


class _FakeTerm:
    def __init__(self, name, children=None):
        self.display_name = name
        self.children = children or _FakeTerms()


class _FakeSets:
    def __init__(self, items=None):
        self.items = list(items or [])

    def get(self):
        return self

    def after_execute(self, callback):
        callback(self.items)
        return self

    def ensure(self, name):
        node = _FakeSet(name)
        self.items.append(node)
        return node


class _FakeSet:
    def __init__(self, name, children=None):
        self.display_name = name
        self.children = children or _FakeTerms()


class _FakeGroups:
    def __init__(self, items=None):
        self.items = list(items or [])

    def get(self):
        return self

    def after_execute(self, callback):
        callback(self.items)
        return self

    def ensure(self, name):
        node = _FakeGroup(name)
        self.items.append(node)
        return node


class _FakeGroup:
    def __init__(self, name, sets=None):
        self.display_name = name
        self.sets = sets or _FakeSets()

    def ensure_set(self, name):
        return self.sets.ensure(name)


EXPECTED_TREE = [
    {
        "name": "G",
        "sets": [
            {
                "name": "S",
                "children": [{"name": "T", "children": [{"name": "T2", "children": []}]}],
            }
        ],
    }
]


def _store_with(groups):
    store = Store(object())
    store._properties["groups"] = groups
    return store


def _sample_tree():
    """Group G -> set S -> term T -> child T2."""
    term = _FakeTerm("T", _FakeTerms([_FakeTerm("T2")]))
    term_set = _FakeSet("S", _FakeTerms([term]))
    group = _FakeGroup("G", _FakeSets([term_set]))
    return _FakeGroups([group])


def test_store_export_tree_delegates_to_manager():
    store = _store_with(_sample_tree())

    assert store.export_tree().value == EXPECTED_TREE


def test_store_import_tree_creates_queued_nodes():
    store = _store_with(_FakeGroups())
    data = [{"name": "G", "sets": [{"name": "S", "children": [{"name": "T"}]}]}]

    returned = store.import_tree(data)

    assert returned is store
    assert [g.display_name for g in store.groups.items] == ["G"]
    group = store.groups.items[0]
    assert [s.display_name for s in group.sets.items] == ["S"]
    assert [t.display_name for t in group.sets.items[0].children.items] == ["T"]
