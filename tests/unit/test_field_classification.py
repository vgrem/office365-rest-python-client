"""What a SharePoint column holds, answered by the column.

A ``fields`` read that omits ``FieldTypeKind`` hands back base ``Field`` objects, so a
caller cannot ask the Python class what a column is. These are the facts the column
states instead — the same ones the migration's typed-value remapping asks for.
"""

from __future__ import annotations

import pytest
from office365.migration.offline import offline_context
from office365.sharepoint.fields.field import Field, is_taxonomy_column, schema_property
from office365.sharepoint.fields.lookup import FieldLookup

#: The questions a caller may ask of a column.
_PREDICATES = ("is_taxonomy", "is_lookup", "is_person", "is_multi_valued", "is_multi_choice", "is_value_object")

_TAXONOMY_SCHEMA = (
    '<Field Type="Note" DisplayName="Topics"><Customization><ArrayOfProperty>'
    '<Property><Name>SspId</Name><Value xmlns:p4="y" p4:type="q1:Guid">caf48611-0000</Value></Property>'
    "<Property><Name>TermSetId</Name><Value>9f3a1b2c-4d5e-6f70-8192-a3b4c5d6e7f8</Value></Property>"
    "</ArrayOfProperty></Customization></Field>"
)


def column(**members) -> Field:
    """A column as a ``fields`` projection returns it."""
    return Field(offline_context()).hydrate(members)


@pytest.mark.parametrize(
    ("members", "expected"),
    [
        ({}, set()),
        ({"TypeAsString": "Text"}, set()),
        ({"TypeAsString": "Lookup"}, {"is_lookup"}),
        ({"TypeAsString": "LookupMulti"}, {"is_lookup", "is_multi_valued"}),
        ({"TypeAsString": "User"}, {"is_person"}),
        ({"TypeAsString": "UserMulti"}, {"is_person", "is_multi_valued"}),
        # A column created from a ``Type="Lookup" Mult="TRUE"`` schema keeps the
        # single-value spelling, and only the flag tells the truth (live-verified).
        ({"TypeAsString": "Lookup", "AllowMultipleValues": True}, {"is_lookup", "is_multi_valued"}),
        ({"TypeAsString": "MultiChoice"}, {"is_multi_valued", "is_multi_choice"}),
        # A column created from a ``Type="Choice" Mult="TRUE"`` schema reads back as
        # "Choice" and stores one value, so the schema's ``Mult`` flag is not trusted.
        ({"TypeAsString": "Choice", "SchemaXml": 'Mult="TRUE"'}, set()),
        ({"TypeAsString": "TaxonomyFieldType"}, {"is_taxonomy"}),
        ({"TypeAsString": "TaxonomyFieldTypeMulti"}, {"is_taxonomy", "is_multi_valued"}),
        ({"TypeAsString": "URL"}, {"is_value_object"}),
    ],
)
def test_a_column_says_what_it_holds(members, expected):
    field = column(**members)

    assert {name for name in _PREDICATES if getattr(field, name)} == expected


def test_a_schema_that_names_a_term_set_makes_a_column_managed_metadata():
    """``TypeAsString`` alone misses a managed-metadata column replayed from a schema."""
    schema_bound = column(TypeAsString="Note", SchemaXml=_TAXONOMY_SCHEMA)

    assert schema_bound.is_taxonomy is True
    assert schema_property(schema_bound.schema_xml, "TermSetId") == "9f3a1b2c-4d5e-6f70-8192-a3b4c5d6e7f8"
    assert schema_property(schema_bound.schema_xml, "SspId") == "caf48611-0000"
    assert schema_property(schema_bound.schema_xml, "Absent") is None
    assert schema_property(None, "TermSetId") is None
    assert column(TypeAsString="Note").is_taxonomy is False
    assert is_taxonomy_column(None, _TAXONOMY_SCHEMA) is True


def test_a_multiple_values_flag_is_declared_on_a_column_not_on_a_lookup():
    """The flag belongs to every column: a User column carries it too (live-verified)."""
    assert Field.odata_name("allow_multiple_values") == "AllowMultipleValues"
    assert FieldLookup.odata_name("allow_multiple_values") == "AllowMultipleValues"
