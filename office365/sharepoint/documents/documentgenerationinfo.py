from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.documents.contentassemblyformanswer import (
    ContentAssemblyFormAnswer,
)
from office365.sharepoint.documents.location import DocumentLocation


class DocumentGenerationInfo(ClientValue):
    def __init__(
        self,
        conditional_fields_to_be_deleted: StringCollection = StringCollection(),
        content_assembly_form_answers: ClientValueCollection[ContentAssemblyFormAnswer] = ClientValueCollection(
            ContentAssemblyFormAnswer
        ),
        copy_fields_from_existing_document: bool = None,
        file_name: str = None,
        folder_url: str = None,
        format_: int = None,
        is_temp_file: bool = None,
        temp_file_url: str = None,
        update_folder_permissions: bool = None,
        document_location: DocumentLocation = DocumentLocation(),
    ):
        self.conditional_fields_to_be_deleted = conditional_fields_to_be_deleted
        self.content_assembly_form_answers = content_assembly_form_answers
        self.copy_fields_from_existing_document = copy_fields_from_existing_document
        self.file_name = file_name
        self.folder_url = folder_url
        self.format = format_
        self.is_temp_file = is_temp_file
        self.temp_file_url = temp_file_url
        self.update_folder_permissions = update_folder_permissions
        self.DocumentLocation = document_location
