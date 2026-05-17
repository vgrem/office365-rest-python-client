from typing import Optional

from office365.runtime.client_value import ClientValue


class CommunicationSiteCreationRequest(ClientValue):
    def __init__(
        self,
        title: str,
        url: str,
        description: Optional[str] = None,
        lcid: Optional[str] = None,
        classification: Optional[str] = None,
        allow_filesharing_for_guest_users: Optional[bool] = None,
        web_template_extension_id: Optional[str] = None,
        site_design_id: Optional[str] = None,
        allow_file_sharing_for_guest_users: Optional[bool] = None,
        sensitivity_label: Optional[str] = None,
        sensitivity_label2: Optional[str] = None,
    ):
        """
        Options for configuring the Communication Site that will be created.

        :param str title: Site title
        :param str url: Absolute site url
        :param str description:
        :param str lcid: The LCID (locale identifier) for a site
        """
        self.Title = title
        self.Url = url
        self.Description = description
        self.lcid = lcid
        self.Classification = classification
        self.AllowFileSharingForGuestUsers = allow_filesharing_for_guest_users
        self.WebTemplateExtensionId = web_template_extension_id
        self.SiteDesignId = site_design_id
        self.AllowFileSharingForGuestUsers = allow_file_sharing_for_guest_users
        self.SensitivityLabel = sensitivity_label
        self.SensitivityLabel2 = sensitivity_label2

    @property
    def entity_type_name(self):
        return "SP.Publishing.CommunicationSiteCreationRequest"
