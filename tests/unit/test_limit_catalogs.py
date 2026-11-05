"""The published limit rows: every one is well formed, and every catalog is reachable.

A row is data a caller reads before sending a request — a value, a unit, a scope, a window
and the page it came from — so a malformed one is a wrong budget handed to a person who
cannot check it against the code. And a catalog module that nothing imports still *exists*:
``catalog(product=...)`` answers with an empty list, the docs page that reads it goes blank,
and no request anywhere fails.
"""

from __future__ import annotations

import subprocess
import sys
import unittest

from office365.onedrive.driveitems.driveItem import DriveItem
from office365.onedrive.drives.drive import Drive
from office365.onedrive.permissions.permission import Permission
from office365.outlook.calendar.calendar import Calendar
from office365.outlook.mail.folders.folder import MailFolder
from office365.runtime.limits import LimitKind, catalog, catalog_products, limits_of
from office365.teams.chats.messages.message import ChatMessage

#: What a row may say about the shape of the request it counts.
REQUEST_TYPES = {"", "read", "write", "delete", "any"}


class TestPublishedRows(unittest.TestCase):
    def test_every_row_is_well_formed(self):
        rows = catalog()

        self.assertTrue(rows, "no rows registered - the catalogs registered nothing at all")
        self.assertIn("graph", catalog_products(), "the Graph-wide row is the one every request spends")
        for row in rows:
            with self.subTest(row=str(row)):
                self.assertTrue(row.name)
                self.assertIsInstance(row.kind, LimitKind)
                self.assertGreater(row.value, 0)
                self.assertTrue(row.unit, f"{row.name!r} counts an unnamed unit")
                self.assertIn(row.request_type, REQUEST_TYPES)
                self.assertGreaterEqual(row.window_seconds or 0, 0)
                self.assertTrue(row.doc.startswith("https://"), f"{row.name!r} cites {row.doc!r}")

    def test_one_import_exposes_every_catalog(self):
        """Discovery must not depend on which module a caller happened to touch first.

        A product catalog registers itself when imported, so the aggregator has to import all
        of them; a new ``quotas`` module that nobody adds there would answer ``[]`` for its
        product and vanish from the generated docs without failing anything.
        """
        code = """
import importlib, pkgutil
import office365
from office365.limits import catalog_products

seen = set(catalog_products())
for module in pkgutil.walk_packages(office365.__path__, "office365."):
    if module.name.endswith((".quotas", ".thresholds")):
        importlib.import_module(module.name)
print(sorted(set(catalog_products()) - seen - {"model"}))  # "model" is written by @limit on a class
"""
        result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)

        self.assertEqual(result.stdout.strip(), "[]", f"not imported by office365/limits.py: {result.stdout.strip()}")


class TestBindings(unittest.TestCase):
    """A published row reaches a caller only through the type that spends it.

    Every catalog above can be complete, reachable and correct while a caller who asks a
    model what a request costs gets nothing back: the rows are registered under a product,
    not on the class, and ``limits_of`` reads the class. So the types migration code touches
    most are held to answering rows — and to answering the *published* ones, so a binding
    cannot smuggle in a number nobody can check.
    """

    #: The resources a migration reads most, one per spending hierarchy.
    P1 = (
        DriveItem,  # and everything else on ``BaseItem``
        Drive,
        Permission,
        ChatMessage,
        MailFolder,
        Calendar,
    )

    def test_a_p1_type_answers_the_rows_it_spends(self):
        for target in self.P1:
            with self.subTest(target.__name__):
                self.assertTrue(limits_of(target), f"{target.__name__} declares no limits")

    def test_a_binding_answers_a_published_row(self):
        published = catalog()
        for target in self.P1:
            for decl in limits_of(target):
                with self.subTest(target.__name__, row=str(decl.limit)):
                    self.assertIn(decl.limit, published, f"{target.__name__} declares a row no catalog published")
