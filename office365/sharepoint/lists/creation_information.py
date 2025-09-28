from office365.runtime.client_value import ClientValue
from office365.sharepoint.lists.template_type import ListTemplateType


class ListCreationInformation(ClientValue):
    """Represents metadata about list creation."""

    def __init__(
        self,
        title: str = None,
        description: str = None,
        base_template: ListTemplateType = None,
        allow_content_types: bool = False,
        custom_schema_xml: str = None,
        document_template_type: int = None,
        quick_launch_option: int = None,
        template_feature_id: int = None,
        template_type: int = None,
        data_source_properties: dict = None,
        url: str = None,
    ):
        """
        :param int or None base_template:
        :param bool allow_content_types:
        :poram str or None description: Specifies the description of the new list.
        :param str title: Specifies the display name of the new list.
        :param str custom_schema_xml: Specifies the list schema of the new list.
        :param str document_template_type: Specifies the identifier of the document template for the new list.
        :param int quick_launch_option: Specifies whether the new list is displayed on the Quick Launch of the site
        :param int template_feature_id: Specifies the feature identifier of the feature that contains the list schema
            for the new list. It MUST be empty GUID if the list schema for the new list is not contained within
            a feature.
        :param int template_type: Specifies the list server template of the new list.
        """
        super(ListCreationInformation, self).__init__()
        self.Title = title
        self.Description = description
        self.BaseTemplate = base_template
        self.AllowContentTypes = allow_content_types
        self.CustomSchemaXml = custom_schema_xml
        self.DataSourceProperties = None
        self.DocumentTemplateType = document_template_type
        self.QuickLaunchOption = quick_launch_option
        self.TemplateFeatureId = template_feature_id
        self.TemplateType = template_type
        self.DataSourceProperties = data_source_properties
        self.Url = url

    @property
    def entity_type_name(self):
        return "SP.List"
