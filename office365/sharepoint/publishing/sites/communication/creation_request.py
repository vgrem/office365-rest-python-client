from office365.runtime.client_value import ClientValue


class CommunicationSiteCreationRequest(ClientValue):
    def __init__(
        self,
        title: str,
        url: str,
        description: str = None,
        lcid: str = None,
        classification: str = None,
        allow_filesharing_for_guest_users: bool = None,
        web_template_extension_id: str = None,
        site_design_id: str = None,
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

    @property
    def entity_type_name(self):
        return "SP.Publishing.CommunicationSiteCreationRequest"
