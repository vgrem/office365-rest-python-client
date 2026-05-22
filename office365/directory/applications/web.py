from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.applications.implicitgrantsettings import ImplicitGrantSettings
from office365.directory.applications.redirecturisettings import RedirectUriSettings
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection


@dataclass
class WebApplication(ClientValue):
    """Specifies settings for a web application."""

    homePageUrl: str | None = None
    logoutUrl: str | None = None
    redirectUris: StringCollection = field(default_factory=StringCollection)
    implicitGrantSettings: ImplicitGrantSettings = field(default_factory=ImplicitGrantSettings)
    redirectUriSettings: ClientValueCollection[RedirectUriSettings] = field(
        default_factory=lambda: ClientValueCollection(RedirectUriSettings)
    )

    @property
    def entity_type_name(self):
        return "microsoft.graph.WebApplication"
