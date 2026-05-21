from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class CommunicationSiteCreationRequest(ClientValue):
    """Options for configuring the Communication Site that will be created.

    :param str title: Site title
    :param str url: Absolute site url
    :param str description:
    :param str lcid: The LCID (locale identifier) for a site
    """

    Title: str
    Url: str
    Description: str | None = None
    lcid: str | None = None
    Classification: str | None = None
    AllowFileSharingForGuestUsers: bool | None = None
    WebTemplateExtensionId: str | None = None
    SiteDesignId: str | None = None
    SensitivityLabel: str | None = None
    SensitivityLabel2: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.CommunicationSiteCreationRequest"
