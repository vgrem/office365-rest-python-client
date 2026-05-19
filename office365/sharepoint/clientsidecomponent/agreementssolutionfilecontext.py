from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.documents.destinationlibraryinfo import (
    DestinationLibraryInfo,
)
from office365.sharepoint.documents.effectivebasepermissions import (
    EffectiveBasePermissions,
)
from office365.sharepoint.documents.librarydetails import LibraryDetails


@dataclass
class AgreementsSolutionFileContext(ClientValue):
    category_id: str | None = None
    category_term_set_id: str | None = None
    check_out_type: int | None = None
    current_version: str | None = None
    does_user_have_edit_permission_on_parent: bool | None = None
    effective_base_permissions: EffectiveBasePermissions = field(default_factory=EffectiveBasePermissions)
    field_library: LibraryDetails = field(default_factory=LibraryDetails)
    file_properties: dict | None = None
    file_relative_path: str | None = None
    folder_path_full_url: str | None = None
    is_agreements_solution_file: bool | None = None
    last_published_version: str | None = None
    list_id: str | None = None
    list_item_id: str | None = None
    list_item_properties: dict | None = None
    list_item_unique_id: str | None = None
    modern_template_library: LibraryDetails | None = None
    parent_library: LibraryDetails | None = None
    site_id: str | None = None
    snippet_library: LibraryDetails | None = None
    target_library: DestinationLibraryInfo | None = None
    web_id: str | None = None
    web_server_relative_url: str | None = None
    web_url: str | None = None
