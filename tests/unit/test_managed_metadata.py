"""Offline tests for Managed Metadata (taxonomy) field handling.

Covers the base-library fixes that make a taxonomy column usable: the field is
created without a ``List`` attribute (so its ``LookupList`` binds to the web's
hidden TaxonomyHiddenList) and a multi-value collection is actually populated.
The write onto the hidden note companion column needs a real column, so it is
covered in ``tests/sharepoint/test_taxonomy.py``.

The term store export/import walk over the same managed-metadata types lives here
too — export reads a store tree, import replays it into queued creates.
"""

from __future__ import annotations

from office365.graph_client import GraphClient
from office365.runtime.http.http_method import HttpMethod
from office365.sharepoint.taxonomy.create_xml_parameters import TaxonomyFieldCreateXmlParameters
from office365.sharepoint.taxonomy.field_value import TaxonomyFieldValue
from office365.sharepoint.taxonomy.field_value_col import TaxonomyFieldValueCollection
from tests._scripted_transport import RecordingTransport


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


def test_set_taxonomy_collection_populates_items():
    terms = TaxonomyFieldValueCollection([TaxonomyFieldValue(Label="TermA", TermGuid="a" * 8)])
    assert len(terms) == 1
    assert terms[0].TermGuid == "aaaaaaaa"


# --- The term store: export reads a tree, import replays it ------------------------------------------------


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


def _graph_store(payloads):
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    transport = RecordingTransport(payloads)
    client.pending_request().transport = transport
    return client.sites["site-id"].term_store, transport


def _term(term_id, name):
    return {"id": term_id, "labels": [{"name": name, "languageTag": "en-US", "isDefault": True}]}


def test_store_export_tree_traverses_real_graph_objects():
    store, transport = _graph_store(
        [
            {"value": [{"id": "g", "displayName": "G"}]},
            {"value": [{"id": "s", "localizedNames": [{"name": "S", "languageTag": "en-US"}]}]},
            {"value": [_term("t", "T")]},
            {"value": [_term("t2", "T2")]},
            {"value": []},
        ]
    )

    result = store.export_tree()
    assert transport.calls == 0
    assert result.value == []
    result.execute_query()

    assert result.value == EXPECTED_TREE
    assert [request.method for request in transport.requests] == [HttpMethod.Get] * 5
    assert transport.urls[0].endswith("/termStore/groups")
    assert "/groups/g/sets" in transport.urls[1]
    assert "/sets/s/children" in transport.urls[2]
    assert "/terms/t/children" in transport.urls[3]
    assert "/terms/t2/children" in transport.urls[4]


def test_store_import_tree_creates_queued_nodes():
    store, transport = _graph_store(
        [
            {"id": "g", "displayName": "G"},
            {"id": "s", "localizedNames": [{"name": "S", "languageTag": "en-US"}]},
            _term("t", "T"),
            _term("t2", "T2"),
        ]
    )

    returned = store.import_tree(EXPECTED_TREE)

    assert returned is store
    assert transport.calls == 0
    store.execute_query()

    assert [request.method for request in transport.requests] == [HttpMethod.Post] * 4
    assert transport.urls[0].endswith("/termStore/groups")
    assert "/groups/g/sets" in transport.urls[1]
    assert "/sets/s/children" in transport.urls[2]
    assert "/terms/t/children" in transport.urls[3]
    assert transport.requests[0].data["displayName"] == "G"
    assert transport.requests[1].data["localizedNames"][0]["name"] == "S"
    assert transport.requests[2].data["labels"][0]["name"] == "T"
    assert transport.requests[3].data["labels"][0]["name"] == "T2"
