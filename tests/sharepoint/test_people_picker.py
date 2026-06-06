from __future__ import annotations

from tests import test_user_principal_name
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSPPeoplePicker(SPTestCase):
    """People picker tests"""

    def test_01_client_people_picker_resolve_user(self):
        """Resolve a user via client people picker"""
        result = (
            self.client.client_people_picker.client_people_picker_resolve_user(self.client, test_user_principal_name)
        ).execute_query()
        self.assertIsNotNone(result.value)

    # def test2_get_picker_entity_information(self):
    #    result = self.client.client_people_picker.get_picker_entity_information(self.client,
    #                                                                         test_user_principal_name).execute_query()
    #    self.assertIsNotNone(result.value)

    def test_02_get_search_results(self):
        """Search for users using the people picker"""
        result = self.client.people_picker.get_search_results(self.client, "Doe").execute_query()
        self.assertIsNotNone(result.value)
