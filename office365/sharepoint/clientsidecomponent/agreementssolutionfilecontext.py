from office365.runtime.client_value import ClientValue
from office365.sharepoint.documents.destinationlibraryinfo import (
    DestinationLibraryInfo,
)
from office365.sharepoint.documents.effectivebasepermissions import (
    EffectiveBasePermissions,
)
from office365.sharepoint.documents.librarydetails import LibraryDetails
from typing import Optional


class AgreementsSolutionFileContext(ClientValue):
    def __init__(
        self,
        category_id: Optional[str] = None,
        category_term_set_id: Optional[str] = None,
        check_out_type: Optional[int] = None,
        current_version: Optional[str] = None,
        does_user_have_edit_permission_on_parent: Optional[bool] = None,
        effective_base_permissions: EffectiveBasePermissions = EffectiveBasePermissions(),
        field_library: LibraryDetails = LibraryDetails(),
        file_properties: Optional[dict] = None,
        file_relative_path: Optional[str] = None,
        folder_path_full_url: Optional[str] = None,
        is_agreements_solution_file: Optional[bool] = None,
        last_published_version: Optional[str] = None,
        list_id: Optional[str] = None,
        list_item_id: Optional[str] = None,
        list_item_properties: Optional[dict] = None,
        list_item_unique_id: Optional[str] = None,
        modern_template_library: Optional[LibraryDetails] = None,
        parent_library: Optional[LibraryDetails] = None,
        site_id: Optional[str] = None,
        snippet_library: Optional[LibraryDetails] = None,
        target_library: Optional[DestinationLibraryInfo] = None,
        web_id: Optional[str] = None,
        web_server_relative_url: Optional[str] = None,
        web_url: Optional[str] = None,
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
