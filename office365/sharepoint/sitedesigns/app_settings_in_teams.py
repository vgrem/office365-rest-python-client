from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sitedesigns.desktop_settings import DesktopSettings
from office365.sharepoint.sitedesigns.mobile_settings import MobileSettings


class AppSettingsInTeams(ClientValue):
    DesktopSettings: DesktopSettings = field(default_factory=DesktopSettings)
    MobileSettings: MobileSettings = field(default_factory=MobileSettings)
