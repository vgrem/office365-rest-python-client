"""The script family: five collections, one scope set, and no stable-root counterpart.

None of these exists on ``v1.0`` - the metadata declares them under ``beta`` - so every test
here addresses the beta client. All five want ``DeviceManagementScripts``; the app under test
does not hold it, so they skip today with the set named, and run unchanged once it is granted.

Two of the five (``deviceHealthScripts``, ``deviceComplianceScripts``) refuse with a bare
``403`` that names no scope. The declaration then rests on the family the segment belongs to,
which is why the docstrings say which ones were measured and which were inferred.
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestScripts(GraphDelegatedTestCase):
    """What an administrator pushes to a device as code."""

    @requires_delegated("DeviceManagementScripts.Read.All", "DeviceManagementScripts.ReadWrite.All")
    def test_01_platform_scripts_are_listed(self):
        """``deviceManagementScripts`` is the platform script family (measured refusal)."""
        scripts = self.client_beta.device_management.device_management_scripts
        self.assertTrue(str(scripts.resource_path).endswith("/deviceManagementScripts"))

        scripts.top(5).get().execute_query()

    @requires_delegated("DeviceManagementScripts.Read.All", "DeviceManagementScripts.ReadWrite.All")
    def test_02_shell_scripts_are_listed(self):
        """``deviceShellScripts`` is the shell script family (measured refusal)."""
        scripts = self.client_beta.device_management.device_shell_scripts
        self.assertTrue(str(scripts.resource_path).endswith("/deviceShellScripts"))

        scripts.top(5).get().execute_query()

    @requires_delegated("DeviceManagementScripts.Read.All", "DeviceManagementScripts.ReadWrite.All")
    def test_03_custom_attribute_scripts_are_listed(self):
        """A custom attribute script writes a value back into Entra (measured refusal)."""
        scripts = self.client_beta.device_management.device_custom_attribute_shell_scripts
        self.assertTrue(str(scripts.resource_path).endswith("/deviceCustomAttributeShellScripts"))

        scripts.top(5).get().execute_query()

    @requires_delegated("DeviceManagementScripts.Read.All", "DeviceManagementScripts.ReadWrite.All")
    def test_04_health_scripts_are_listed(self):
        """``deviceHealthScripts`` is remediation: it detects and then repairs (inferred)."""
        scripts = self.client_beta.device_management.device_health_scripts
        self.assertTrue(str(scripts.resource_path).endswith("/deviceHealthScripts"))

        scripts.top(5).get().execute_query()

    @requires_delegated("DeviceManagementScripts.Read.All", "DeviceManagementScripts.ReadWrite.All")
    def test_05_compliance_scripts_are_listed(self):
        """A compliance script runs on the device to grade its posture (inferred)."""
        scripts = self.client_beta.device_management.device_compliance_scripts
        self.assertTrue(str(scripts.resource_path).endswith("/deviceComplianceScripts"))

        scripts.top(5).get().execute_query()
