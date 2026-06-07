from __future__ import annotations

from typing import ClassVar, Optional

from office365.sharepoint.navigation.nodes.collection import NavigationNodeCollection
from office365.sharepoint.navigation.nodes.creationinformation import (
    NavigationNodeCreationInformation,
)
from office365.sharepoint.navigation.nodes.node import NavigationNode
from office365.sharepoint.navigation.publishing_navigation_provider_type import PublishingNavigationProviderType

from tests.sharepoint.sharepoint_case import SPTestCase


class TestNavigation(SPTestCase):
    """SharePoint navigation tests"""

    target_node: ClassVar[Optional[NavigationNode]] = None

    def test_01_list_navigation_nodes(self):
        """List all navigation nodes in the Quick Launch"""
        result = self.client.web.navigation.quick_launch.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_02_is_global_nav_enabled(self):
        """Check if global navigation is enabled"""
        result = self.client.navigation_service.global_nav_enabled().execute_query()
        self.assertIsNotNone(result.value)

    def test_03_get_web_navigation(self):
        """Get web navigation with top navigation bar"""
        result = self.client.web.navigation.expand(["TopNavigationBar"]).get().execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertIsInstance(result.top_navigation_bar, NavigationNodeCollection)

    def test_04_create_navigation_node(self):
        """Create a navigation node in the Quick Launch"""
        node_create_info = NavigationNodeCreationInformation(
            "Technical documentation",
            "https://docs.microsoft.com/en-us/documentation/",
            True,
        )
        new_node = self.client.web.navigation.quick_launch.add(node_create_info).execute_query()
        self.assertIsNotNone(new_node.resource_path)
        TestNavigation.target_node = new_node

    def test_05_get_navigation_node_by_id(self):
        """Get a navigation node by ID"""
        self.assertIsNotNone(TestNavigation.target_node)
        node_id = TestNavigation.target_node.properties.get("Id")
        self.assertIsNotNone(node_id)
        result = self.client.web.navigation.quick_launch.get_by_id(int(node_id)).get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_06_get_navigation_node_by_index(self):
        """Get a navigation node by index"""
        result = self.client.web.navigation.quick_launch.get_by_index(0).get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_07_delete_navigation_node(self):
        """Delete a navigation node and verify"""
        self.assertIsNotNone(TestNavigation.target_node)
        node_id = TestNavigation.target_node.properties.get("Id")
        TestNavigation.target_node.delete_object().execute_query()
        # Verify deletion by confirming no node with that ID exists
        result = self.client.web.navigation.quick_launch.get().execute_query()
        self.assertFalse(any(n.properties.get("Id") == node_id for n in result))

    def test_08_get_publishing_navigation_provider_type(self):
        """Get the publishing navigation provider type"""
        result = self.client.navigation_service.get_publishing_navigation_provider_type().execute_query()
        self.assertIsInstance(result.value, PublishingNavigationProviderType)
