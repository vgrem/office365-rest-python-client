from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class PublicClientApplication(ClientValue):
    """
    Specifies settings for non-web app or non-web API (for example, mobile or other public clients such as an
    installed application running on a desktop device).
    """

    redirectUris: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self):
        return "microsoft.graph.PublicClientApplication"
