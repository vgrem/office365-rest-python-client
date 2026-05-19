from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class XmlSchemaFieldCreationInformation(ClientValue):
    """Specifies metadata about a field

    Fields:
        SchemaXml (str | None): Specifies the schema that defines the field
        Options (int | None): Specifies the control settings that are used while adding a field
    """

    SchemaXml: str | None = None
    Options: int | None = None

    @property
    def entity_type_name(self):
        return "SP.XmlSchemaFieldCreationInformation"
