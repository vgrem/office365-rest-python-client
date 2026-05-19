import uuid
from typing import Optional

from office365.graph_client import GraphClient
from office365.onedrive.termstore.groups.group import Group
from office365.onedrive.termstore.sets.set import Set
from office365.onedrive.termstore.store import Store
from office365.onedrive.termstore.terms.term import Term
from tests import test_client_id, test_client_secret, test_root_site_url, test_tenant
from tests.decorators import requires_delegated_permission_or_role
from tests.graph_case import GraphDelegatedTestCase


class TestTermStore(GraphDelegatedTestCase):
    target_store: Optional[Store] = None
    target_group: Optional[Group] = None
    target_set: Optional[Set] = None
    target_term: Optional[Term] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
        cls.target_store = client.sites.get_by_url(test_root_site_url).term_store

    @requires_delegated_permission_or_role("Sites.Read.All", "Sites.ReadWrite.All", roles=["Global Administrator"])
    def test1_list_groups(self):
        """List term store groups"""
        assert self.target_store is not None
        result = self.target_store.groups.top(1).get().execute_query()
        self.assertLessEqual(len(result), 1)
        for group in result:
            self.assertIsNotNone(group.resource_path)

    @requires_delegated_permission_or_role("Sites.Read.All", "Sites.ReadWrite.All", roles=["Global Administrator"])
    def test2_create_group(self):
        """Create a term store group"""
        group_name = "Group_" + uuid.uuid4().hex
        assert self.target_store is not None
        new_group = self.target_store.groups.add(group_name).execute_query()
        assert new_group.resource_path is not None
        TestTermStore.target_group = new_group

    @requires_delegated_permission_or_role("Sites.Read.All", "Sites.ReadWrite.All", roles=["Global Administrator"])
    def test3_get_group_by_name(self):
        """Get a term store group by name"""
        name = TestTermStore.target_group
        assert name is not None
        name = name.display_name
        assert name is not None
        assert self.target_store is not None
        group = self.target_store.groups.get_by_name(name).get().execute_query()
        self.assertIsNotNone(group.resource_path)

    @requires_delegated_permission_or_role("Sites.Read.All", "Sites.ReadWrite.All", roles=["Global Administrator"])
    def test4_create_set(self):
        """Create a term store set"""
        set_name = "Set_" + uuid.uuid4().hex
        assert TestTermStore.target_group is not None
        new_set = TestTermStore.target_group.sets.add(set_name).execute_query()
        assert new_set.resource_path is not None
        TestTermStore.target_set = new_set

    @requires_delegated_permission_or_role("Sites.Read.All", "Sites.ReadWrite.All", roles=["Global Administrator"])
    def test5_list_sets(self):
        """List term store sets"""
        assert TestTermStore.target_group is not None
        sets = TestTermStore.target_group.sets.get().execute_query()
        self.assertIsNotNone(sets.resource_path)
        self.assertGreaterEqual(1, len(sets))

    @requires_delegated_permission_or_role("Sites.Read.All", "Sites.ReadWrite.All", roles=["Global Administrator"])
    def test6_create_term(self):
        """Create a term in a term store set"""
        label_name = "Term_" + uuid.uuid4().hex
        assert TestTermStore.target_set is not None
        new_term = TestTermStore.target_set.children.add(label_name).execute_query()
        assert new_term.resource_path is not None
        TestTermStore.target_term = new_term

    @requires_delegated_permission_or_role("Sites.Read.All", "Sites.ReadWrite.All", roles=["Global Administrator"])
    def test7_list_terms(self):
        """List terms in a term store set"""
        assert TestTermStore.target_set is not None
        terms = TestTermStore.target_set.terms.get().execute_query()
        self.assertIsNotNone(terms.resource_path)
        self.assertGreaterEqual(1, len(terms))

    @requires_delegated_permission_or_role("Sites.Read.All", "Sites.ReadWrite.All", roles=["Global Administrator"])
    def test8_delete_term(self):
        """Delete a term"""
        assert TestTermStore.target_term is not None
        TestTermStore.target_term.delete_object().execute_query()

    @requires_delegated_permission_or_role("Sites.Read.All", "Sites.ReadWrite.All", roles=["Global Administrator"])
    def test9_delete_set(self):
        """Delete a term store set"""
        assert TestTermStore.target_set is not None
        TestTermStore.target_set.delete_object().execute_query()

    @requires_delegated_permission_or_role("Sites.Read.All", "Sites.ReadWrite.All", roles=["Global Administrator"])
    def test_10_delete_group(self):
        """Delete a term store group"""
        assert TestTermStore.target_group is not None
        TestTermStore.target_group.delete_object().execute_query()
