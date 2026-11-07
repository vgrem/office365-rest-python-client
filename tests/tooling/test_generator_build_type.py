"""A type whose module this run has not created yet is resolvable, not shadowed.

Deliberately not covered here: the model itself, or any generated file. What is pinned
is one branch of the builder that only the beta snapshot can reach -- a member whose
type routes into a package that the run is about to create. ``importlib.util.find_spec``
raises ``ModuleNotFoundError`` for such a name instead of returning ``None``, so the
shadow check has to survive it; before it did, a dry run of ``metadata/GraphBeta.xml``
aborted on ``office365.security.dlp.*`` (94 lookups) instead of finishing.
"""

from __future__ import annotations

from unittest import TestCase

from generator.build.type import TypeBuilder


class TestAShadowCheckSurvivesAMissingParent(TestCase):
    def test_01_a_module_under_a_package_that_does_not_exist_yet_is_not_a_shadow(self):
        """The regression: `find_spec` raises here, and the builder must not."""
        self.assertFalse(TypeBuilder._is_shadowed("office365.security.dlp.name_value_pair"))
        self.assertFalse(TypeBuilder._is_shadowed("office365.security.securitycopilot.plugin_setting"))

    def test_02_a_real_package_is_still_reported_as_a_shadow(self):
        """`office365.security` is a package, so `office365.security.py` cannot exist."""
        self.assertTrue(TypeBuilder._is_shadowed("office365.security"))

    def test_03_a_real_module_is_not_a_shadow(self):
        self.assertFalse(TypeBuilder._is_shadowed("office365.entity"))
