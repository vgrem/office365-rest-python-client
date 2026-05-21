from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.lists.templates.type import ListTemplateType


@dataclass
class ListCreationInformation(ClientValue):
    """Represents metadata about list creation."""

    Title: Optional[str] = None
    Description: Optional[str] = None
    BaseTemplate: Optional[ListTemplateType] = None
    AllowContentTypes: bool = False
    CustomSchemaXml: Optional[str] = None
    DataSourceProperties: Optional[dict] = None
    DocumentTemplateType: Optional[int] = None
    QuickLaunchOption: Optional[int] = None
    TemplateFeatureId: Optional[int] = None
    TemplateType: Optional[int] = None
    Url: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.List"
