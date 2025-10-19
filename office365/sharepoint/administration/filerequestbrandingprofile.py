from uuid import UUID

from office365.runtime.client_value import ClientValue


class FileRequestBrandingProfile(ClientValue):

    def __init__(
        self,
        background_file_id: UUID = None,
        background_file_name: str = None,
        background_file_url: str = None,
        logo_file_id: UUID = None,
        logo_file_name: str = None,
        logo_file_url: str = None,
        profile_type: int = None,
    ):
        self.BackgroundFileId = background_file_id
        self.BackgroundFileName = background_file_name
        self.BackgroundFileUrl = background_file_url
        self.LogoFileId = logo_file_id
        self.LogoFileName = logo_file_name
        self.LogoFileUrl = logo_file_url
        self.ProfileType = profile_type

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.FileRequestBrandingProfile"
