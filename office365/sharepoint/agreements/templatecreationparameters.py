from typing import Optional

from office365.runtime.client_value import ClientValue


class TemplateCreationParameters(ClientValue):
    def __init__(
        self,
        source_file_unique_id: Optional[str] = None,
        source_library_id: Optional[str] = None,
        template_name: Optional[str] = None,
    ):
        self.SourceFileUniqueId = source_file_unique_id
        self.SourceLibraryId = source_library_id
        self.TemplateName = template_name

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Agreements.Models.TemplateCreationParameters"
