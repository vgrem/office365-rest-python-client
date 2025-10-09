from office365.runtime.client_value import ClientValue


class TemplateCreationParameters(ClientValue):

    def __init__(
        self,
        source_file_unique_id: str = None,
        source_library_id: str = None,
        template_name: str = None,
    ):
        self.SourceFileUniqueId = source_file_unique_id
        self.SourceLibraryId = source_library_id
        self.TemplateName = template_name

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Agreements.Models.TemplateCreationParameters"
