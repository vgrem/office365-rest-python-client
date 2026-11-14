"""The script family: five collections, one scope set, and no stable-root counterpart.

None of these exists on ``v1.0`` - the metadata declares them under ``beta`` - so every test
here addresses ``self.dm_beta``. All five want ``DeviceManagementScripts``; the app under test
does not hold it, so they skip today with the set named, and run unchanged once it is granted.

Two of the five (``deviceHealthScripts``, ``deviceComplianceScripts``) refuse with a bare
``403`` that names no scope. The declaration then rests on the family the segment belongs to,
which is why the docstrings say which ones were measured and which were inferred.
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.intune.intune_case import SCRIPTS, IntuneCase


class TestScripts(IntuneCase):
    """What an administrator pushes to a device as code."""

    @requires_delegated(*SCRIPTS)
    def test_01_platform_scripts_are_listed(self):
        """``deviceManagementScripts`` is the platform script family (measured refusal)."""
        self.read(self.dm_beta.device_management_scripts, "deviceManagementScripts")

    @requires_delegated(*SCRIPTS)
    def test_02_shell_scripts_are_listed(self):
        """``deviceShellScripts`` is the shell script family (measured refusal)."""
        self.read(self.dm_beta.device_shell_scripts, "deviceShellScripts")

    @requires_delegated(*SCRIPTS)
    def test_03_custom_attribute_scripts_are_listed(self):
        """A custom attribute script writes a value back into Entra (measured refusal)."""
        self.read(self.dm_beta.device_custom_attribute_shell_scripts, "deviceCustomAttributeShellScripts")

    @requires_delegated(*SCRIPTS)
    def test_04_health_scripts_are_listed(self):
        """``deviceHealthScripts`` is remediation: it detects and then repairs (inferred)."""
        self.read(self.dm_beta.device_health_scripts, "deviceHealthScripts")

    @requires_delegated(*SCRIPTS)
    def test_05_compliance_scripts_are_listed(self):
        """A compliance script runs on the device to grade its posture (inferred)."""
        self.read(self.dm_beta.device_compliance_scripts, "deviceComplianceScripts")
