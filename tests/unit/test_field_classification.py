"""What a SharePoint column holds, answered by the column itself.

A ``fields`` read that omits ``FieldTypeKind`` hands back base ``Field`` objects, so a caller
cannot ask the Python class what a column is: it asks the column, and the answer is the row
SharePoint returned - ``TypeAsString``, ``AllowMultipleValues``, the schema. Each case below is
one column shape as the migration's typed-value remapping meets it.
"""

from __future__ import annotations

from office365.migration.offline import offline_context
from office365.runtime.schema import TypeSchema
from office365.sharepoint.fields.field import Field, is_taxonomy_column, schema_property
from office365.sharepoint.fields.lookup import FieldLookup
from office365.sharepoint.fields.user import FieldUser
from office365.sharepoint.taxonomy.field import TaxonomyField

_TAXONOMY_SCHEMA = (
    '<Field Type="Note" DisplayName="Topics"><Customization><ArrayOfProperty>'
    '<Property><Name>SspId</Name><Value xmlns:p4="y" p4:type="q1:Guid">caf48611-0000</Value></Property>'
    "<Property><Name>TermSetId</Name><Value>9f3a1b2c-4d5e-6f70-8192-a3b4c5d6e7f8</Value></Property>"
    "</ArrayOfProperty></Customization></Field>"
)


def projection(**members) -> Field:
    """A column as ``web.fields`` returns it: a base ``Field``, no ``FieldTypeKind``."""
    return Field(offline_context()).hydrate(members)


def test_a_text_column_holds_a_scalar_and_asks_nothing_of_the_remapper():
    text = projection(TypeAsString="Text")

    assert text.type_as_string == "Text"
    assert not any(
        (
            text.is_lookup,
            text.is_person,
            text.is_taxonomy,
            text.is_multi_valued,
            text.is_multi_choice,
            text.is_value_object,
        )
    )


def test_a_lookup_column_points_at_an_item_in_another_list():
    lookup = projection(TypeAsString="Lookup", LookupList="6b6c1a9e-0000", LookupField="Title")

    assert lookup.is_lookup
    assert not lookup.is_multi_valued  # one id, so the id is remapped in place
    assert not lookup.is_person


def test_a_multi_lookup_is_declared_by_its_flag_not_by_its_type_spelling():
    """Live-verified: a ``Type="Lookup" Mult="TRUE"`` column reads back as the single spelling.

    Only ``AllowMultipleValues`` tells the truth, and a column misread as single-value keeps a
    collection of *source* item ids on the target.
    """
    multi_lookup = projection(TypeAsString="Lookup", AllowMultipleValues=True)

    assert multi_lookup.is_lookup
    assert multi_lookup.is_multi_valued


def test_the_only_column_that_stores_many_choices_is_the_multi_choice_one():
    """Live-probed: a ``Type="Choice" Mult="TRUE"`` column reads back as ``"Choice"``.

    It stores one value in a single ``nvarchar`` slot, so its schema's ``Mult`` flag is not
    trusted - the flag lies in one direction only.
    """
    multi_choice = projection(TypeAsString="MultiChoice")
    choice_with_mult = projection(TypeAsString="Choice", SchemaXml='Mult="TRUE"')

    assert multi_choice.is_multi_valued
    assert multi_choice.is_multi_choice
    assert not choice_with_mult.is_multi_valued
    assert not choice_with_mult.is_multi_choice


def test_a_person_column_holds_a_site_user():
    person = projection(TypeAsString="User")

    assert person.is_person
    assert not person.is_lookup


def test_a_hyperlink_column_holds_a_value_object_rather_than_a_string():
    """``{"Url", "Description"}`` - a scalar projection dropped it, and a string write broke reads."""
    hyperlink = projection(TypeAsString="URL")

    assert hyperlink.is_value_object


def test_a_schema_that_names_a_term_set_makes_a_column_managed_metadata():
    """``TypeAsString`` alone misses a managed-metadata column replayed from a schema."""
    schema_bound = projection(TypeAsString="Note", SchemaXml=_TAXONOMY_SCHEMA)

    assert schema_bound.is_taxonomy is True
    assert schema_property(schema_bound.schema_xml, "TermSetId") == "9f3a1b2c-4d5e-6f70-8192-a3b4c5d6e7f8"
    assert schema_property(schema_bound.schema_xml, "SspId") == "caf48611-0000"
    assert schema_property(schema_bound.schema_xml, "Absent") is None
    assert schema_property(None, "TermSetId") is None
    assert projection(TypeAsString="TaxonomyFieldTypeMulti").is_multi_valued
    assert projection(TypeAsString="Note").is_taxonomy is False
    assert is_taxonomy_column(None, _TAXONOMY_SCHEMA) is True


def test_a_lookup_declares_where_it_points_and_a_base_column_declares_nothing():
    """Where the metadata puts them: ``SP.FieldLookup``, and its subclasses by inheritance.

    Declaring them on ``Field`` would say every column has a lookup list: ``SP.Field`` carries
    none of them, ``SP.FieldLookup`` all three.
    """
    assert TypeSchema.of(FieldLookup).name_of("lookup_list") == "LookupList"
    assert TypeSchema.of(FieldLookup).name_of("lookup_field") == "LookupField"
    assert TypeSchema.of(FieldLookup).name_of("allow_multiple_values") == "AllowMultipleValues"
    assert TypeSchema.of(TaxonomyField).name_of("text_field_id") == "TextField"
    # Inherited, not re-spelled: SP.FieldUser and SP.Taxonomy.TaxonomyField are lookups.
    assert TypeSchema.of(FieldUser).name_of("lookup_list") == "LookupList"
    assert TypeSchema.of(TaxonomyField).name_of("allow_multiple_values") == "AllowMultipleValues"
    # ...and a base column declares none of them.
    assert not {"lookup_list", "lookup_field", "text_field_id"} & set(Field._schema.by_attr)

    lookup = FieldLookup(offline_context()).hydrate({"LookupList": "6b6c1a9e-0000", "LookupField": "Title"})
    term_column = TaxonomyField(offline_context()).hydrate({"TextField": "0f8a-0000"})

    assert (lookup.lookup_list, lookup.lookup_field) == ("6b6c1a9e-0000", "Title")
    assert term_column.text_field_id == "0f8a-0000"
