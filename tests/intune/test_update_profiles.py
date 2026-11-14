"""Update profiles and tunnels: the preview-root families the Intune portal is built on.

Windows update profiles (feature, quality, driver) and the Microsoft Tunnel configuration have
no ``v1.0`` segment, so every read here names the beta client. All four are licensed by Intune
Plan 1 rather than gated by an extra scope: the tenant's *user* may hold the plan at
``PendingInput`` and the segments still answer, which is why no licence guard appears here.
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestWindowsUpdateProfiles(GraphDelegatedTestCase):
    """Three ways to steer Windows Update, three collections."""

    @requires_delegated("DeviceManagementConfiguration.Read.All", "DeviceManagementConfiguration.ReadWrite.All")
    def test_01_feature_update_profiles_are_listed(self):
        """A feature update profile pins the Windows version a ring moves to."""
        profiles = self.client_beta.device_management.windows_feature_update_profiles
        self.assertTrue(str(profiles.resource_path).endswith("/windowsFeatureUpdateProfiles"))

        profiles.top(5).get().execute_query()

    @requires_delegated("DeviceManagementConfiguration.Read.All", "DeviceManagementConfiguration.ReadWrite.All")
    def test_02_quality_update_profiles_are_listed(self):
        """A quality update profile defers or expedites the monthly patch."""
        profiles = self.client_beta.device_management.windows_quality_update_profiles
        self.assertTrue(str(profiles.resource_path).endswith("/windowsQualityUpdateProfiles"))

        profiles.top(5).get().execute_query()

    @requires_delegated("DeviceManagementConfiguration.Read.All", "DeviceManagementConfiguration.ReadWrite.All")
    def test_03_driver_update_profiles_are_listed(self):
        """A driver update profile approves a driver per device class, not per device."""
        profiles = self.client_beta.device_management.windows_driver_update_profiles
        self.assertTrue(str(profiles.resource_path).endswith("/windowsDriverUpdateProfiles"))

        profiles.top(5).get().execute_query()


class TestMicrosoftTunnel(GraphDelegatedTestCase):
    """Tunnel configurations and the sites that serve them."""

    @requires_delegated("DeviceManagementConfiguration.Read.All", "DeviceManagementConfiguration.ReadWrite.All")
    def test_01_tunnel_configurations_are_listed(self):
        """A tunnel configuration is the tenant-wide server-network definition."""
        configurations = self.client_beta.device_management.microsoft_tunnel_configurations
        self.assertTrue(str(configurations.resource_path).endswith("/microsoftTunnelConfigurations"))

        configurations.top(5).get().execute_query()

    @requires_delegated("DeviceManagementConfiguration.Read.All", "DeviceManagementConfiguration.ReadWrite.All")
    def test_02_tunnel_sites_are_listed(self):
        """A site is one region's collection of tunnel servers."""
        sites = self.client_beta.device_management.microsoft_tunnel_sites
        self.assertTrue(str(sites.resource_path).endswith("/microsoftTunnelSites"))

        sites.top(5).get().execute_query()
