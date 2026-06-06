from __future__ import annotations

from tests.sharepoint.sharepoint_case import SPTestCase


class TestFlow(SPTestCase):
    """SharePoint flow tests"""

    def test_01_get_flow_permission_level(self):
        """Get flow permission level for default library"""
        lib = self.client.web.default_document_library()
        result = lib.get_flow_permission_level().execute_query()
        self.assertIsNotNone(result.value)
