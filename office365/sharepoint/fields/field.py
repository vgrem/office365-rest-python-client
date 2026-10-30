from __future__ import annotations

import re
from typing import Optional, Type, Union

from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.converters.scalars import parse_enum
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.fields.type import FieldType
from office365.sharepoint.thresholds import Limits, limit
from office365.sharepoint.translation.user_resource import UserResource

#: ``TypeAsString`` spellings, grouped by the question a caller asks of a column. A column's
#: Python class is decided by whichever of ``FieldTypeKind``/``TypeAsString`` a read happened to
#: project (``resolve_field_type``), so "what does this column hold" is answered from its
#: spelling rather than its class.
TAXONOMY_FIELD_TYPES = frozenset({"TaxonomyFieldType", "TaxonomyFieldTypeMulti"})
LOOKUP_FIELD_TYPES = frozenset({"Lookup", "LookupMulti"})
PERSON_FIELD_TYPES = frozenset({"User", "UserMulti"})
CHOICE_FIELD_TYPES = frozenset({"Choice", "MultiChoice"})
MULTI_VALUE_FIELD_TYPES = frozenset({"LookupMulti", "UserMulti", "MultiChoice", "TaxonomyFieldTypeMulti"})

#: One ``<Property><Name>..</Name><Value>..</Value></Property>`` row of a schema's
#: ``<Customization>`` bag (a managed metadata column's ``TermSetId``, ``SspId``, ...).
_CUSTOMIZATION_PROPERTY = re.compile(
    r"<Name>\s*(?P<name>[^<]+?)\s*</Name>\s*<Value\b[^>]*>\s*(?P<value>[^<\s]+)\s*</Value>",
    re.IGNORECASE,
)


def schema_property(schema_xml: Optional[str], name: str) -> Optional[str]:
    """Read one value out of a field schema's ``<Customization>`` property bag.

    A managed metadata column keeps its term set binding in the schema, not in a
    projected member: ``TermSetId``/``SspId`` are not columns of ``SP.Field``, and a
    structure captured for replay carries the schema only. Reading them here keeps the
    one spelling of the bag.
    """
    if not schema_xml:
        return None
    for match in _CUSTOMIZATION_PROPERTY.finditer(schema_xml):
        if match.group("name").lower() == name.lower():
            return match.group("value")
    return None


def is_taxonomy_column(type_as_string: Optional[str], schema_xml: Optional[str]) -> bool:
    """Whether a column is Managed Metadata (bound to a term set).

    ``TypeAsString`` is the direct answer for a column SharePoint provisioned as one;
    a column whose schema names a ``TermSetId`` is one whatever the type says. Both
    callers -- a live :class:`Field` and a replayed structure definition -- ask here.
    """
    return type_as_string in TAXONOMY_FIELD_TYPES or "TermSetId" in (schema_xml or "")


#: What a column may hold: the length of a single line of text, and how many terms a managed
#: metadata column is expected to carry before downstream experiences stop being guaranteed.
@limit(Limits.TEXT_COLUMN, Limits.DEFAULT_TERMS)
class Field(Entity):
    """A container for metadata within a SharePoint list and associated list items."""

    def __str__(self):
        return self.title or self.entity_type_name

    def __repr__(self):
        return self.internal_name or self.id or self.entity_type_name

    @staticmethod
    def resolve_field_type(type_id_or_name: Union[str, int, FieldType]) -> Type[Field]:
        from office365.sharepoint.fields.calculated import FieldCalculated
        from office365.sharepoint.fields.choice import FieldChoice
        from office365.sharepoint.fields.computed import FieldComputed
        from office365.sharepoint.fields.currency import FieldCurrency
        from office365.sharepoint.fields.date_time import FieldDateTime
        from office365.sharepoint.fields.guid import FieldGuid
        from office365.sharepoint.fields.lookup import FieldLookup
        from office365.sharepoint.fields.multi_choice import FieldMultiChoice
        from office365.sharepoint.fields.multi_line_text import FieldMultiLineText
        from office365.sharepoint.fields.text import FieldText
        from office365.sharepoint.fields.url import FieldUrl
        from office365.sharepoint.fields.user import FieldUser
        from office365.sharepoint.taxonomy.field import TaxonomyField

        field_known_types: dict[FieldType, Type[Field]] = {
            FieldType.Text: FieldText,
            FieldType.Calculated: FieldCalculated,
            FieldType.Choice: FieldChoice,
            FieldType.MultiChoice: FieldMultiChoice,
            FieldType.Lookup: FieldLookup,
            FieldType.User: FieldUser,
            FieldType.Computed: FieldComputed,
            FieldType.URL: FieldUrl,
            FieldType.Guid: FieldGuid,
            FieldType.Currency: FieldCurrency,
            FieldType.Note: FieldMultiLineText,
            FieldType.DateTime: FieldDateTime,
        }
        if isinstance(type_id_or_name, FieldType):
            return field_known_types.get(type_id_or_name, Field)
        if isinstance(type_id_or_name, int):
            type_enum = parse_enum(FieldType, type_id_or_name)
            if type_enum is not None:
                return field_known_types.get(type_enum, Field)  # type: ignore[arg-type]
            return Field
        elif type_id_or_name in {"TaxonomyFieldType", "TaxonomyFieldTypeMulti"}:
            return TaxonomyField
        elif type_id_or_name == "Thumbnail":
            from office365.sharepoint.fields.thumbnail import FieldThumbnail

            return FieldThumbnail
        else:
            return Field

    @property
    def is_taxonomy(self) -> bool:
        """Whether the column is Managed Metadata (bound to a term set)."""
        return is_taxonomy_column(self.type_as_string, self.schema_xml)

    @property
    def is_lookup(self) -> bool:
        """Whether the column stores a reference to an item in another list."""
        return self.type_as_string in LOOKUP_FIELD_TYPES

    @property
    def is_person(self) -> bool:
        """Whether the column stores a SharePoint user."""
        return self.type_as_string in PERSON_FIELD_TYPES

    @property
    def is_multi_valued(self) -> bool:
        """Whether the column holds many values (a multi-lookup, -person, -choice or -term).

        ``TypeAsString`` is not authoritative here. A column created from a
        ``Type="Lookup" Mult="TRUE"`` (or ``Type="User" Mult="TRUE"``) schema keeps that
        spelling, so SharePoint reports the *single-value* type and only
        ``AllowMultipleValues`` tells the truth (live-verified). Classifying such a column
        as single-value left its collection of ids unremapped: a multi-lookup kept source
        item ids and a multi-person kept source site-user ids on the target.

        The flag is declared on ``FieldLookup`` (and inherited by ``FieldUser`` and
        ``TaxonomyField``) because that is where ``SP.FieldLookup`` puts it; a column of
        any other type reports it as ``None``, so this predicate -- which answers for
        every column -- reads the row rather than a getter it cannot have.
        """
        return self.type_as_string in MULTI_VALUE_FIELD_TYPES or self.properties.get("AllowMultipleValues") is True

    @property
    def is_multi_choice(self) -> bool:
        """Whether the column stores a collection of choice values.

        ``TypeAsString == "MultiChoice"`` is the reliable signal. Live-probed: a column
        created from a ``Type="Choice" Mult="TRUE"`` schema reads back as ``"Choice"``,
        stores one value in a single ``nvarchar`` slot (a scalar write round-trips, an
        array is rejected), so its schema ``Mult`` flag is deliberately not used.
        """
        return self.type_as_string in CHOICE_FIELD_TYPES and self.is_multi_valued

    @property
    def is_value_object(self) -> bool:
        """Whether the column holds a REST value object rather than a scalar.

        A Hyperlink column is the common case: a read returns
        ``{"Url": ..., "Description": ...}``, which a scalar-only record projection
        dropped (a plain string is accepted on write but then makes every subsequent
        *read* of the column fail, live-probed).
        """
        return self.type_as_string == "URL"

    def enable_index(self) -> ClientResult[bool]:
        """
        Enables the index for a field
        An index speeds up queries on the indexed fields as well as sorting and grouping operations
        """
        return_type = ClientResult(self.context, bool())
        qry = ServiceOperationQuery(self, "enableIndex", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    def disable_index(self) -> ClientResult[bool]:
        """
        Disables the index for a field
        """
        return_type = ClientResult[bool](self.context)
        qry = ServiceOperationQuery(self, "disableIndex", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    def set_show_in_display_form(self, flag) -> Self:
        """Sets the value of the ShowInDisplayForm property for this fields.

        Args:
            flag (bool):
        """
        qry = ServiceOperationQuery(self, "setShowInDisplayForm", [flag])
        self.context.add_query(qry)
        return self

    def set_show_in_edit_form(self, flag):
        """Sets the value of the ShowInEditForm property for this fields.

        Args:
            flag (bool): A Boolean value that indicates whether this field is shown in the edit form.
        """
        qry = ServiceOperationQuery(self, "setShowInEditForm", [flag])
        self.context.add_query(qry)

    def set_show_in_new_form(self, flag: bool) -> Self:
        """Sets the value of the ShowInNewForm property for this fields.

        Args:
            flag (bool): A Boolean value that indicates whether this field is shown in the new form.
        """
        qry = ServiceOperationQuery(self, "setShowInNewForm", [flag])
        self.context.add_query(qry)
        return self

    @odata(name="Id")
    @property
    def id(self) -> Optional[str]:
        """Gets a value that specifies the field identifier."""
        return self.properties.get("Id", None)

    @odata(name="AutoIndexed")
    @property
    def auto_indexed(self) -> Optional[bool]:
        """Gets a Boolean value that specifies whether the field is auto-indexed."""
        return self.properties.get("AutoIndexed", None)

    @odata(name="DefaultFormula")
    @property
    def default_formula(self) -> Optional[str]:
        return self.properties.get("DefaultFormula", None)

    @odata(name="FieldTypeKind")
    @property
    def field_type_kind(self) -> FieldType:
        return self.properties.get("FieldTypeKind", FieldType.Unknown)

    @odata(name="DescriptionResource", navigation=True)
    @property
    def description_resource(self) -> UserResource:
        """Gets the resource object corresponding to the Description property for a field"""
        return self.properties.get(
            "DescriptionResource",
            UserResource(self.context, ResourcePath("DescriptionResource", self.resource_path)),
        )

    @odata(name="SchemaXml")
    @property
    def schema_xml(self) -> Optional[str]:
        """
        Gets a value that specifies the XML schema that defines the field.
        """
        return self.properties.get("SchemaXml", None)

    @schema_xml.setter
    def schema_xml(self, val: str):
        """Sets a value that specifies the XML schema that defines the field."""
        self.set_property("SchemaXml", val)

    def schema_xml_for_copy(self) -> Optional[str]:
        """Return :attr:`schema_xml` prepared for ``CreateFieldAsXml`` on another site.

        A schema copied verbatim carries its origin-specific ``SourceID`` and
        ``Version`` attributes. SharePoint rejects such a payload with
        "The object has been updated by another user since it was last
        fetched" (while still creating the field); removing those attributes
        lets the copy complete cleanly. Returns ``None`` when the schema is
        not loaded.
        """
        xml = self.schema_xml
        if xml is None:
            return None
        return re.sub(r'\s*(?:SourceID|Version)="[^"]*"', "", xml)

    @odata(name="TypeAsString")
    @property
    def type_as_string(self) -> Optional[str]:
        """Gets a value that specifies the type of the field"""
        return self.properties.get("TypeAsString", None)

    @odata(name="Title")
    @property
    def title(self) -> Optional[str]:
        """Gets a value that specifies the display name of the field."""
        return self.properties.get("Title", None)

    @title.setter
    def title(self, val: str):
        """
        Sets a value that specifies the display name of the field.
        """
        self.set_property("Title", val)

    @odata(name="Group")
    @property
    def group(self) -> Optional[str]:
        """Gets a value that specifies the field group"""
        return self.properties.get("Group", None)

    @group.setter
    def group(self, val):
        """Sets a value that specifies the field group."""
        self.set_property("Group", val)

    @odata(name="InternalName")
    @property
    def internal_name(self) -> Optional[str]:
        """Gets a value that specifies the field internal name."""
        return self.properties.get("InternalName", None)

    @odata(name="CanBeDeleted")
    @property
    def can_be_deleted(self) -> Optional[bool]:
        """Gets a value that specifies whether the field can be deleted"""
        return self.properties.get("CanBeDeleted", None)

    @odata(name="ClientSideComponentId", beta=True)
    @property
    def client_side_component_id(self) -> Optional[str]:
        return self.properties.get("ClientSideComponentId", None)

    @odata(name="ClientSideComponentProperties", beta=True)
    @property
    def client_side_component_properties(self) -> Optional[str]:
        return self.properties.get("ClientSideComponentProperties", None)

    @odata(name="ClientValidationFormula")
    @property
    def client_validation_formula(self) -> Optional[str]:
        return self.properties.get("ClientValidationFormula", None)

    @property
    def enforce_unique_values(self) -> Optional[bool]:
        """
        Specifies whether the field enforces unique values.
        """
        return self.properties.get("enforceUniqueValues", None)

    @odata(name="Filterable")
    @property
    def filterable(self) -> Optional[bool]:
        """
        Specifies whether list items in the list can be filtered by the field value.
        """
        return self.properties.get("Filterable", None)

    @odata(name="FromBaseType")
    @property
    def from_base_type(self) -> Optional[bool]:
        """
        Gets a Boolean value that indicates whether the field derives from a base field type.
        """
        return self.properties.get("FromBaseType", None)

    @odata(name="JSLink")
    @property
    def js_link(self) -> Optional[str]:
        """
        When implemented in a derived class, gets or sets the name of an external JavaScript file that contains
        any client rendering logic for fields of the derived type.
        """
        return self.properties.get("JSLink", None)

    @odata(name="Hidden")
    @property
    def hidden(self) -> Optional[bool]:
        """
        Gets a value that specifies whether the field is hidden in list views and list forms.
        """
        return self.properties.get("Hidden", None)

    @hidden.setter
    def hidden(self, val):
        """
        Sets a value that specifies whether the field is hidden in list views and list forms.
        """
        self.set_property("Hidden", val)

    @odata(name="NoCrawl")
    @property
    def no_crawl(self) -> Optional[bool]:
        """
        Gets value that specifies whether the field can be crawled by a search engine.
        """
        return self.properties.get("NoCrawl", None)

    @odata(name="ReadOnlyField")
    @property
    def read_only_field(self) -> Optional[bool]:
        """
        Specifies whether the value of the field is read-only.
        """
        return self.properties.get("ReadOnlyField", None)

    @odata(name="DefaultValue")
    @property
    def default_value(self) -> Optional[str]:
        """
        Gets  a value that specifies the default value for the field.
        """
        return self.properties.get("DefaultValue", None)

    @default_value.setter
    def default_value(self, val):
        """
        Sets a value that specifies the default value for the field.
        """
        self.set_property("DefaultValue", val)

    @odata(name="Indexed")
    @property
    def indexed(self) -> bool:
        return self.properties.get("Indexed", None)

    def ensure_indexed(self) -> Self:
        """Ensure this field is indexed (idempotent, deferred).

        Indexing a column lets queries filter/sort on it past the 5,000-item list
        view threshold. Run with ``execute_query()``.
        """

        def _enable(_=None) -> None:
            if self.indexed is not True:
                self.enable_index()

        if self.indexed is None:
            self.ensure_property("Indexed").after_execute(_enable)
        else:
            _enable()
        return self

    @odata(name="TypeDisplayName")
    @property
    def type_display_name(self) -> Optional[str]:
        """
        Gets a value that specifies the display name for the type of the field.
        """
        return self.properties.get("TypeDisplayName", None)

    @odata(name="TitleResource", navigation=True)
    @property
    def title_resource(self):
        """Gets the resource object corresponding to the Title property for a field"""
        return self.properties.get(
            "TitleResource",
            UserResource(self.context, ResourcePath("TitleResource", self.resource_path)),
        )

    @odata(name="TypeShortDescription")
    @property
    def type_short_description(self) -> Optional[str]:
        """
        Gets a value that specifies the description for the type of the field.
        """
        return self.properties.get("TypeShortDescription", None)

    def set_property(self, name, value, persist_changes=True):
        super().set_property(name, value, persist_changes)
        # fallback: create a new resource path
        if name == "FieldTypeKind":
            self.__class__ = self.resolve_field_type(value)  # type: ignore[reportAttributeAccessIssue]
        elif name == "TypeAsString" and self.properties.get("FieldTypeKind") in (None, 0, FieldType.Invalid):
            # taxonomy fields report an "Invalid" field kind, so the type name
            # (e.g. "TaxonomyFieldType") is the reliable signal
            self.__class__ = self.resolve_field_type(value)  # type: ignore[reportAttributeAccessIssue]
        return self

    @odata(name="AutofillInfo", beta=True)
    @property
    def autofill_info(self) -> Optional[str]:
        """Gets the AutofillInfo property"""
        return self.properties.get("AutofillInfo", None)

    @odata(name="ClientValidationMessage")
    @property
    def client_validation_message(self) -> Optional[str]:
        """Gets the ClientValidationMessage property"""
        return self.properties.get("ClientValidationMessage", None)

    @odata(name="CustomFormatter", beta=True)
    @property
    def custom_formatter(self) -> Optional[str]:
        """Gets the CustomFormatter property"""
        return self.properties.get("CustomFormatter", None)

    @odata(name="Description")
    @property
    def description(self) -> Optional[str]:
        """Gets the Description property"""
        return self.properties.get("Description", None)

    @odata(name="Direction")
    @property
    def direction(self) -> Optional[str]:
        """Gets the Direction property"""
        return self.properties.get("Direction", None)

    @odata(name="EntityPropertyName")
    @property
    def entity_property_name(self) -> Optional[str]:
        """Gets the EntityPropertyName property"""
        return self.properties.get("EntityPropertyName", None)

    @odata(name="IndexStatus")
    @property
    def index_status(self) -> Optional[int]:
        """Gets the IndexStatus property"""
        return self.properties.get("IndexStatus", None)

    @odata(name="IsModern")
    @property
    def is_modern(self) -> Optional[bool]:
        """Gets the IsModern property"""
        return self.properties.get("IsModern", None)

    @odata(name="PinnedToFiltersPane", beta=True)
    @property
    def pinned_to_filters_pane(self) -> Optional[bool]:
        """Gets the PinnedToFiltersPane property"""
        return self.properties.get("PinnedToFiltersPane", None)

    @odata(name="Required")
    @property
    def required(self) -> Optional[bool]:
        """Gets the Required property"""
        return self.properties.get("Required", None)

    @odata(name="SchemaXmlWithResourceTokens")
    @property
    def schema_xml_with_resource_tokens(self) -> Optional[str]:
        """Gets the SchemaXmlWithResourceTokens property"""
        return self.properties.get("SchemaXmlWithResourceTokens", None)

    @odata(name="Scope")
    @property
    def scope(self) -> Optional[str]:
        """Gets the Scope property"""
        return self.properties.get("Scope", None)

    @odata(name="Sealed")
    @property
    def sealed(self) -> Optional[bool]:
        """Gets the Sealed property"""
        return self.properties.get("Sealed", None)

    @odata(name="ShowInFiltersPane", beta=True)
    @property
    def show_in_filters_pane(self) -> Optional[int]:
        """Gets the ShowInFiltersPane property"""
        return self.properties.get("ShowInFiltersPane", None)

    @odata(name="Sortable")
    @property
    def sortable(self) -> Optional[bool]:
        """Gets the Sortable property"""
        return self.properties.get("Sortable", None)

    @odata(name="StaticName")
    @property
    def static_name(self) -> Optional[str]:
        """Gets the StaticName property"""
        return self.properties.get("StaticName", None)

    @odata(name="ValidationFormula")
    @property
    def validation_formula(self) -> Optional[str]:
        """Gets the ValidationFormula property"""
        return self.properties.get("ValidationFormula", None)

    @odata(name="ValidationMessage")
    @property
    def validation_message(self) -> Optional[str]:
        """Gets the ValidationMessage property"""
        return self.properties.get("ValidationMessage", None)
