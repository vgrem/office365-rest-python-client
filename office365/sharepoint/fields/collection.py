from typing import TYPE_CHECKING, Optional, Union

from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.create_entity import CreateEntityQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.fields.calculated import FieldCalculated
from office365.sharepoint.fields.creation_information import FieldCreationInformation
from office365.sharepoint.fields.date_time import FieldDateTime
from office365.sharepoint.fields.field import Field, T
from office365.sharepoint.fields.geolocation import FieldGeolocation
from office365.sharepoint.fields.number import FieldNumber
from office365.sharepoint.fields.text import FieldText
from office365.sharepoint.fields.type import FieldType
from office365.sharepoint.fields.url import FieldUrl
from office365.sharepoint.fields.user import FieldUser
from office365.sharepoint.fields.xmlSchemaFieldCreationInformation import (
    XmlSchemaFieldCreationInformation,
)
from office365.sharepoint.taxonomy.field import TaxonomyField
from office365.sharepoint.taxonomy.sets.set import TermSet
from office365.sharepoint.taxonomy.stores.store import TermStore

if TYPE_CHECKING:
    from office365.sharepoint.lists.list import List
    from office365.sharepoint.webs.web import Web


class FieldCollection(EntityCollection[Field]):
    """Represents a collection of Field resource."""

    def __init__(self, context, resource_path=None, parent=None):
        super(FieldCollection, self).__init__(context, Field, resource_path, parent)

    def add_calculated(
        self, title: str, formula: str, description: str = None
    ) -> FieldCalculated:
        """
        Creates a Calculated field
        :param str title: Specifies the display name of the field
        :param str formula: Specifies the formula for the field
        :param str or None description: Specifies the description of the field
        """
        return_type = self.add(
            FieldCreationInformation(
                title=title,
                formula=formula,
                field_type_kind=FieldType.Calculated,
                description=description,
            )
        )
        return return_type

    def add_datetime(self, title, description=None):
        # type: (str, Optional[str]) -> FieldDateTime
        """
        Creates DateTime field
        :param str title: Specifies the display name of the field
        :param str or None description: Specifies the description of the field
        """
        return_type = self.add(
            FieldCreationInformation(
                title=title,
                description=description,
                field_type_kind=FieldType.DateTime,
            )
        )
        return return_type

    def add_geolocation_field(self, title, description=None):
        # type: (str, Optional[str]) -> FieldGeolocation
        """
        Creates Geolocation field

        :param str title: Specifies the display name of the field
        :param str or None description: Specifies the description of the field
        """
        return_type = self.add(
            FieldCreationInformation(
                title=title,
                description=description,
                field_type_kind=FieldType.Geolocation,
            )
        )
        return return_type

    def add_number(self, title, description=None):
        # type: (str, Optional[str]) -> FieldNumber
        """
        Creates Number field
        :param str title: Specifies the display name of the field
        :param str or None description: Specifies the description of the field
        """
        return_type = self.add(
            FieldCreationInformation(
                title=title,
                description=description,
                field_type_kind=FieldType.Number,
            )
        )
        return return_type

    def add_url_field(self, title, description=None):
        # type: (str, Optional[str]) -> FieldUrl
        """
        Creates Url field
        :param str title: Specifies the display name of the field
        :param str or None description:
        """
        return self.add(
            FieldCreationInformation(
                title=title, description=description, field_type_kind=FieldType.URL
            )
        )

    def add_lookup_field(
        self, title, lookup_list, lookup_field_name, allow_multiple_values=False
    ):
        """
        Creates a Lookup field

        :param bool allow_multiple_values: Flag determines whether to create multi lookup field or not
        :param str lookup_field_name: Specifies the name of the field in the other data source when creating
            a lookup field
        :param str or office365.sharepoint.lists.list.List lookup_list: Lookup List object or identifier
        :param str title: Specifies the display name of the field.
        """
        from office365.sharepoint.fields.lookup import FieldLookup
        from office365.sharepoint.lists.list import List  # noqa

        return_type = FieldLookup(self.context)

        def _add_lookup_field(lookup_list_id):
            # type: (str) -> None
            if allow_multiple_values:
                field_schema = """
                        <Field Type="LookupMulti" Mult="TRUE" DisplayName="{title}" Required="FALSE" Hidden="TRUE" \
                        ShowField="{lookup_field_name}" List="{{{lookup_list_id}}}" StaticName="{title}" Name="{title}">
                        </Field>
                        """.format(
                    title=title,
                    lookup_field_name=lookup_field_name,
                    lookup_list_id=lookup_list_id,
                )
                self.create_field_as_xml(field_schema, return_type=return_type)
            else:
                self.add_field(
                    FieldCreationInformation(
                        title=title,
                        lookup_list_id=lookup_list_id,
                        lookup_field_name=lookup_field_name,
                        field_type_kind=FieldType.Lookup,
                    ),
                    return_type=return_type,
                )

        if isinstance(lookup_list, List):

            def _lookup_list_loaded():
                _add_lookup_field(lookup_list.id)

            lookup_list.ensure_property("Id", _lookup_list_loaded)
        else:
            _add_lookup_field(lookup_list)
        return return_type

    def add_choice_field(self, title, values, multiple_values=False):
        """
        Creates a Choice field

        :param bool multiple_values:
        :param list[str] values:
        :param str title: Specifies the display name of the field.
        """
        fld_type = FieldType.MultiChoice if multiple_values else FieldType.Choice
        create_field_info = FieldCreationInformation(title, fld_type)
        [create_field_info.Choices.add(choice) for choice in values]
        return self.add_field(create_field_info)

    def add_user_field(self, title):
        # type: (str) -> FieldUser
        """
        Creates a User field

        :param str title: Specifies the display name of the field
        """
        return self.add_field(FieldCreationInformation(title, FieldType.User))

    def add_text_field(self, title: str) -> FieldText:
        """
        Creates a Text field
        :param str title: specifies the display name of the field
        """
        return self.add_field(FieldCreationInformation(title, FieldType.Text))

    def add_dependent_lookup_field(
        self, display_name: str, primary_lookup_field_id: str, show_field: bool
    ) -> Field:
        """Adds a secondary lookup field to a field collection (target).
        Args:
            display_name (str): title of the added field in the target FieldCollection.
            primary_lookup_field_id (str): ID of the main lookup-field in the target to
                associate the dependent lookup field with.
            show_field (str): name of the field from the source list to include data from.
        Returns:
            Field: reference to the SP.Field that was added.
        """
        return_type = Field(self.context)
        self.add_child(return_type)
        parameters = {
            "displayName": display_name,
            "primaryLookupFieldId": primary_lookup_field_id,
            "showField": show_field,
        }
        qry = ServiceOperationQuery(
            self, "AddDependentLookupField", None, parameters, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def add(self, field_create_information: FieldCreationInformation) -> T:
        """Adds a fields to the fields collection.

        :type field_create_information: FieldCreationInformation
        """
        return_type = Field.create_field(self.context, field_create_information)
        self.add_child(return_type)
        qry = CreateEntityQuery(self, return_type, return_type)
        self.context.add_query(qry)
        return return_type

    def add_field(self, parameters: FieldCreationInformation, return_type=None) -> T:
        """Adds a fields to the fields collection.

        :type parameters: FieldCreationInformation
        :param Field or None return_type: Return type
        """
        if return_type is None:
            return_type = Field(self.context)
        self.add_child(return_type)
        payload = {"parameters": parameters}
        qry = ServiceOperationQuery(self, "AddField", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def create_taxonomy_field(
        self,
        name: str,
        term_set: Union[str, TermSet],
        allow_multiple_values: bool = False,
    ) -> TaxonomyField:
        """
        Creates a Taxonomy field

        :param str name: Field name
        :param str or TermSet term_set: TermSet identifier or object
        :param bool allow_multiple_values: Specifies whether the column will allow more than one value
        """
        return_type = TaxonomyField(self.context)

        def _create_taxonomy_field(term_store_id: str, term_set_id: str):
            TaxonomyField.create(
                self,
                name,
                term_set_id,
                term_store_id,
                allow_multiple_values,
                return_type=return_type,
            )

        def _term_store_loaded(term_store: TermStore) -> None:
            if isinstance(term_set, TermSet):

                def _term_set_loaded():
                    _create_taxonomy_field(term_store.id, term_set.id)

                term_set.ensure_property("id", _term_set_loaded)
            else:
                _create_taxonomy_field(term_store.id, term_set)

        self.context.load(self.context.taxonomy.term_store).after_query_execute(
            _term_store_loaded
        )

        return return_type

    def create_field_as_xml(self, schema_xml: str, return_type: T = None) -> T:
        """
        Creates a field based on the values defined in the parameters input parameter.

        :param str schema_xml: Specifies the schema that defines the field
        :param Field or None return_type: Return type
        """
        if return_type is None:
            return_type = Field(self.context)
        self.add_child(return_type)
        payload = {"parameters": XmlSchemaFieldCreationInformation(schema_xml)}
        qry = ServiceOperationQuery(
            self, "CreateFieldAsXml", None, payload, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def get_by_id(self, id_: str) -> Field:
        """
        Gets the fields with the specified ID.

        :param str id_: The field identifier.
        """
        return Field(
            self.context, ServiceOperationPath("getById", [id_], self.resource_path)
        )

    def get_by_internal_name_or_title(self, value: str) -> Field:
        """Returns the first field in the collection based on the internal name or the title specified
        by the parameter.

        :param str value:  The title or internal name to look up the field (2) by.
        """
        return Field(
            self.context,
            ServiceOperationPath(
                "getByInternalNameOrTitle", [value], self.resource_path
            ),
        )

    def get_by_title(self, title: str) -> Field:
        """
        Returns the first fields object in the collection based on the title of the specified fields.

        :param str title: The title to look up the field by
        """
        return Field(
            self.context,
            ServiceOperationPath("getByTitle", [title], self.resource_path),
        )

    @property
    def parent(self):
        # type: () -> Web|List
        return self._parent
