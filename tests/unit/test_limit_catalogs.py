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

from office365.runtime.limits import LimitKind, catalog, catalog_products

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
