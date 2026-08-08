from __future__ import annotations

import unittest

from office365.graph_client import GraphClient


class TestPolicies(unittest.TestCase):
    def test_identity_security_defaults_enforcement_policy_path(self):
        policy = GraphClient().policies.identity_security_defaults_enforcement_policy
        self.assertEqual(str(policy.resource_path), "/policies/identitySecurityDefaultsEnforcementPolicy")
