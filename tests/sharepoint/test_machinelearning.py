from __future__ import annotations

from tests.sharepoint.sharepoint_case import SPTestCase


class TestMachineLearningHub(SPTestCase):
    """Machine learning hub tests"""

    def test_01_enabled(self):
        """Check if machine learning is enabled"""
        result = self.client.machine_learning.machine_learning_enabled.get().execute_query()
        self.assertIsNotNone(result)
