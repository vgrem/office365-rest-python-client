from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SiteCreationProperties(ClientValue):
    """Sets the initial properties for a new site when it is created.

    :param str owner: Gets or sets the login name of the owner of the new site
    :param str url: Gets or sets the new site's URL.
    :param str template: Gets or sets the web template name of the new site.
    :param str site_uni_name:
    """

    Url: str | None = None
    Owner: str | None = None
    OwnerName: str | None = None
    Title: str | None = None
    Template: str | None = None
    SiteUniName: str | None = None
    CompatibilityLevel: int | None = None
    Lcid: str | None = None
    TimeZoneId: int | None = None
    EnableAgreementsSolution: bool | None = None
    StorageMaximumLevel: int | None = None
    StorageWarningLevel: int | None = None
    UserCodeMaximumLevel: float | None = None
    UserCodeWarningLevel: float | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteCreationProperties"
