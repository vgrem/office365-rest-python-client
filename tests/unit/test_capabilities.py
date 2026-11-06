"""One type's four families of fact, asked once.

No tenant shows this: a tenant answers whether *a particular* request succeeded, not
whether the four declarations about a type agree with each other. The aggregation is
therefore pinned here - the exit test is that one call answers every family for a
type - together with the two rules the aggregation adds, which are about the MRO and
about licences, not about the wire.
"""

from __future__ import annotations

import unittest

from office365.capabilities import capabilities_of
from office365.communications.callrecords.collection import CallRecordCollection
from office365.onedrive.driveitems.driveItem import DriveItem
from office365.outlook.mail.messages.message import Message
from office365.permissions.declaration import require_permission


class TestOneCallAnswersEveryFamily(unittest.TestCase):
    """The exit test: shape, permissions, limits and query rules from one call."""

    def test_a_collection_answers_shape_limits_and_query_rules(self):
        caps = capabilities_of(CallRecordCollection)

        self.assertEqual(caps.name, "office365.communications.callrecords.collection:CallRecordCollection")
        # A collection has no columns of its own; the columns belong to the type it collects.
        self.assertEqual(caps.schema.columns, ())
        self.assertEqual(len(caps.limits), 4)
        self.assertFalse(caps.queries.supports("top"))
        self.assertIn("get_direct_routing_calls", caps.declarations)

    def test_an_entity_answers_its_declarations_and_no_query_rules(self):
        caps = capabilities_of(DriveItem)

        self.assertGreater(len(caps.schema.columns), 0)
        self.assertGreater(len(caps.declarations), 0)
        self.assertTrue(caps.declarations["get"].application)
        self.assertEqual(len(caps.limits), 9)
        # Query rules are the collection's, and a drive item is not a collection.
        self.assertIsNone(caps.queries)

    def test_one_call_answers_for_itself(self):
        caps = capabilities_of(Message.send)

        self.assertEqual(caps.declarations["send"].delegated, ("Mail.Send",))
        self.assertIsNone(caps.schema)
        self.assertIsNone(caps.queries)


class TestWhatTheAggregationAdds(unittest.TestCase):
    """The two rules that are not a plain read of one declaration."""

    def test_an_override_that_names_nothing_does_not_hide_the_base(self):
        class Base:
            @require_permission(application=["Sites.Read.All"])
            def read(self):
                """Read."""

        class Child(Base):
            def read(self):
                """Read, restated without a declaration."""

        self.assertEqual(capabilities_of(Child).declarations["read"].application, ("Sites.Read.All",))

    def test_an_override_that_names_something_replaces_the_base(self):
        class Base:
            @require_permission(application=["Sites.Read.All"])
            def read(self):
                """Read."""

        class Child(Base):
            @require_permission(application=["Sites.FullControl.All"])
            def read(self):
                """Read, with its own declaration."""

        self.assertEqual(capabilities_of(Child).declarations["read"].application, ("Sites.FullControl.All",))

    def test_licenses_are_the_union_of_the_plans_named_once_each(self):
        class Mixed:
            @require_permission(application=["Sites.Read.All"], licenses=["SharePoint Online"])
            def read(self):
                """Read."""

            @require_permission(delegated=["Files.Read"], licenses=["Office 365 E3", "SharePoint Online"])
            def write(self):
                """Write."""

        self.assertEqual(capabilities_of(Mixed).licenses, ("Office 365 E3", "SharePoint Online"))

    def test_a_type_that_names_nothing_is_reported_not_refused(self):
        caps = capabilities_of(type("Bare", (), {}))

        self.assertEqual(dict(caps.declarations), {})
        self.assertEqual(caps.licenses, ())
        self.assertEqual(caps.schema.columns, ())

    def test_something_that_is_neither_a_type_nor_a_call_is_refused(self):
        with self.assertRaises(TypeError):
            capabilities_of("DriveItem")


if __name__ == "__main__":
    unittest.main()
