from office365.runtime.client_value import ClientValue
from office365.sharepoint.documents.destinationlibraryinfo import (
    DestinationLibraryInfo,
)
from office365.sharepoint.documents.effectivebasepermissions import (
    EffectiveBasePermissions,
)
from office365.sharepoint.documents.librarydetails import LibraryDetails


class AgreementsSolutionFileContext(ClientValue):

    def __init__(
        self,
        category_id: str = None,
        category_term_set_id: str = None,
        check_out_type: int = None,
        current_version: str = None,
        does_user_have_edit_permission_on_parent: bool = None,
        effective_base_permissions: EffectiveBasePermissions = EffectiveBasePermissions(),
        field_library: LibraryDetails = LibraryDetails(),
        file_properties: dict = None,
        file_relative_path: str = None,
        folder_path_full_url: str = None,
        is_agreements_solution_file: bool = None,
        last_published_version: str = None,
        list_id: str = None,
        list_item_id: str = None,
        list_item_properties: dict = None,
        list_item_unique_id: str = None,
        modern_template_library: LibraryDetails = None,
        parent_library: LibraryDetails = None,
        site_id: str = None,
        snippet_library: LibraryDetails = None,
        target_library: DestinationLibraryInfo = None,
        web_id: str = None,
        web_server_relative_url: str = None,
        web_url: str = None,
    ):
        self.category_id = category_id
        self.category_term_set_id = category_term_set_id
        self.check_out_type = check_out_type
        self.current_version = current_version
        self.does_user_have_edit_permission_on_parent = does_user_have_edit_permission_on_parent
        self.effective_base_permissions = effective_base_permissions
        self.field_library = field_library
        self.file_properties = file_properties
        self.file_relative_path = file_relative_path
        self.folder_path_full_url = folder_path_full_url
        self.is_agreements_solution_file = is_agreements_solution_file
        self.last_published_version = last_published_version
        self.list_id = list_id
        self.list_item_id = list_item_id
        self.list_item_properties = list_item_properties
        self.list_item_unique_id = list_item_unique_id
        self.modern_template_library = modern_template_library
        self.parent_library = parent_library
        self.site_id = site_id
        self.snippet_library = snippet_library
        self.target_library = target_library
        self.web_id = web_id
        self.web_server_relative_url = web_server_relative_url
        self.web_url = web_url
