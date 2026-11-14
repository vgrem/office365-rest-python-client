"""Update profiles and tunnels: the preview-root families the Intune portal is built on.

Windows update profiles (feature, quality, driver) and the Microsoft Tunnel configuration have
no ``v1.0`` segment, so every read here names ``self.dm_beta``. All four are licensed by Intune
Plan 1 rather than gated by an extra scope: the tenant's *user* may hold the plan at
``PendingInput`` and the segments still answer, which is why no licence guard appears here.
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.intune.intune_case import CONFIGURATION, IntuneCase


class TestWindowsUpdateProfiles(IntuneCase):
    """Three ways to steer Windows Update, three collections."""

    @requires_delegated(*CONFIGURATION)
    def test_01_feature_update_profiles_are_listed(self):
        """A feature update profile pins the Windows version a ring moves to."""
        self.read(self.dm_beta.windows_feature_update_profiles, "windowsFeatureUpdateProfiles")

    @requires_delegated(*CONFIGURATION)
    def test_02_quality_update_profiles_are_listed(self):
        """A quality update profile defers or expedites the monthly patch."""
        self.read(self.dm_beta.windows_quality_update_profiles, "windowsQualityUpdateProfiles")

    @requires_delegated(*CONFIGURATION)
    def test_03_driver_update_profiles_are_listed(self):
        """A driver update profile approves a driver per device class, not per device."""
        self.read(self.dm_beta.windows_driver_update_profiles, "windowsDriverUpdateProfiles")


class TestMicrosoftTunnel(IntuneCase):
    """Tunnel configurations and the sites that serve them."""

    @requires_delegated(*CONFIGURATION)
    def test_01_tunnel_configurations_are_listed(self):
        """A tunnel configuration is the tenant-wide server-network definition."""
        self.read(self.dm_beta.microsoft_tunnel_configurations, "microsoftTunnelConfigurations")

    @requires_delegated(*CONFIGURATION)
    def test_02_tunnel_sites_are_listed(self):
        """A site is one region's collection of tunnel servers."""
        self.read(self.dm_beta.microsoft_tunnel_sites, "microsoftTunnelSites")
