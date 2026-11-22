"""A SharePoint column: what shape it is, and the value that shape becomes in Python.

Both answers come from the column, not from the Python class: a ``fields`` read that omits
``FieldTypeKind`` hands back base ``Field`` objects, so ``TypeAsString``, ``AllowMultipleValues``
and the schema are the facts, and ``coerce_field_value`` turns a wire value into the model type
that fact names. The migration's typed-value remapping meets every shape below.
"""

from __future__ import annotations

from datetime import datetime

from office365.migration.offline import offline_context, offline_sharepoint_context
from office365.runtime.converters.named import converter_for
from office365.runtime.schema import TypeSchema
from office365.sharepoint.fields.coercion import coerce_field_value
from office365.sharepoint.fields.field import Field, is_taxonomy_column, schema_property
from office365.sharepoint.fields.geolocation_value import FieldGeolocationValue
from office365.sharepoint.fields.lookup import FieldLookup
from office365.sharepoint.fields.lookup_value import FieldLookupValue
from office365.sharepoint.fields.multi_lookup_value import FieldMultiLookupValue
from office365.sharepoint.fields.multi_user_value import FieldMultiUserValue
from office365.sharepoint.fields.type import FieldType
from office365.sharepoint.fields.url_value import FieldUrlValue
from office365.sharepoint.fields.user import FieldUser
from office365.sharepoint.fields.user_value import FieldUserValue
from office365.sharepoint.listitems.listitem import ListItem
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


# --- what shape a column is --------------------------------------------------------


def test_a_text_column_holds_a_scalar_and_asks_nothing_of_the_remapper() -> None:
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


def test_a_lookup_column_points_at_an_item_in_another_list() -> None:
    lookup = projection(TypeAsString="Lookup", LookupList="6b6c1a9e-0000", LookupField="Title")

    assert lookup.is_lookup
    assert not lookup.is_multi_valued  # one id, so the id is remapped in place
    assert not lookup.is_person


def test_a_multi_lookup_is_declared_by_its_flag_not_by_its_type_spelling() -> None:
    """Live-verified: a ``Type="Lookup" Mult="TRUE"`` column reads back as the single spelling.

    Only ``AllowMultipleValues`` tells the truth, and a column misread as single-value keeps a
    collection of *source* item ids on the target.
    """
    multi_lookup = projection(TypeAsString="Lookup", AllowMultipleValues=True)

    assert multi_lookup.is_lookup
    assert multi_lookup.is_multi_valued


def test_the_only_column_that_stores_many_choices_is_the_multi_choice_one() -> None:
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


def test_a_person_column_holds_a_site_user() -> None:
    person = projection(TypeAsString="User")

    assert person.is_person
    assert not person.is_lookup


def test_a_hyperlink_column_holds_a_value_object_rather_than_a_string() -> None:
    """``{"Url", "Description"}`` - a scalar projection dropped it, and a string write broke reads."""
    assert projection(TypeAsString="URL").is_value_object


def test_a_schema_that_names_a_term_set_makes_a_column_managed_metadata() -> None:
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


def test_a_lookup_declares_where_it_points_and_a_base_column_declares_nothing() -> None:
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


# --- what that column's value becomes ----------------------------------------------


def test_a_person_becomes_a_user_value_from_an_email_an_id_or_a_list() -> None:
    from_email = coerce_field_value(FieldType.User, "alice@contoso.com")
    from_id = coerce_field_value(FieldType.User, 7)
    multi = coerce_field_value(FieldType.User, [1, 2])

    assert isinstance(from_email, FieldUserValue)
    assert from_email.Email == "alice@contoso.com"
    assert from_id.LookupId == 7  # noqa: PLR2004
    assert isinstance(multi, FieldMultiUserValue)
    assert [item.LookupId for item in multi] == [1, 2]


def test_a_url_and_a_geolocation_take_a_string_or_a_pair() -> None:
    plain = coerce_field_value(FieldType.URL, "https://contoso.com")
    pair = coerce_field_value(FieldType.URL, ("https://contoso.com", "Contoso"))

    assert isinstance(plain, FieldUrlValue)
    assert plain.Url == "https://contoso.com"
    assert pair.Description == "Contoso"

    from_string = coerce_field_value(FieldType.Geolocation, "51.5,-0.12")
    from_pair = coerce_field_value(FieldType.Geolocation, (51.5, -0.12))
    assert isinstance(from_string, FieldGeolocationValue)
    assert from_string.Latitude == 51.5  # noqa: PLR2004
    assert from_pair.Longitude == -0.12  # noqa: PLR2004


def test_a_scalar_column_reads_the_text_a_list_carries() -> None:
    assert coerce_field_value(FieldType.Boolean, "yes") is True
    assert coerce_field_value(FieldType.Boolean, "0") is False
    assert coerce_field_value(FieldType.Number, "3.5") == 3.5  # noqa: PLR2004
    assert coerce_field_value(FieldType.Integer, "12") == 12  # noqa: PLR2004
    assert coerce_field_value(FieldType.DateTime, "2024-01-02") == datetime(2024, 1, 2)


def test_a_list_item_persists_the_multi_value_ids_and_not_just_the_names() -> None:
    item = ListItem(offline_sharepoint_context())
    item.set_property("MultiOwner", FieldMultiUserValue([FieldUserValue(12), FieldUserValue(7)]))
    item.set_property("MultiDept", FieldMultiLookupValue([FieldLookupValue(2), FieldLookupValue(3)]))

    # A multi-value column persists its ``<name>Id`` collection; ``<name>`` itself is transient.
    # ``FieldMultiUserValue`` must be handled like ``FieldMultiLookupValue`` (regression: it used
    # to be written as ``<name>`` only, so the user ids were lost).
    assert list(item.properties["MultiOwnerId"]) == [12, 7]
    assert list(item.properties["MultiDeptId"]) == [2, 3]
    assert item.to_json()["MultiOwnerId"] == [12, 7]
    assert item.to_json()["MultiDeptId"] == [2, 3]


def test_a_field_type_resolves_through_the_same_seam_a_named_converter_does() -> None:
    """``converters={col: FieldType}`` and ``schema={col: FieldType}`` are one mechanism.

    A list item's field types are known only at runtime, so ``FieldType`` is the schema a caller
    has; it resolves to the payload coercion above, so the typed-columns path and the generic
    ``converters`` path share one implementation.
    """
    assert converter_for(FieldType.Integer)("42") == 42  # noqa: PLR2004
    assert list(converter_for(FieldType.MultiChoice)("a; b")) == ["a", "b"]
