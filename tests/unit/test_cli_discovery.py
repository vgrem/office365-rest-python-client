"""The level-0 answer is read, not imported.

``o365 graph`` says what one token serves. Answering it by importing the tree costs 5.2 s; the
index the generator ships holds the same list, so the command parses a file (4 ms) and imports
nothing. The test runs the command in a child process, because in this one every package has been
imported by some other test already: what it can assert is the import set of a fresh interpreter.
"""

from __future__ import annotations

import json
import subprocess
import sys
import textwrap

CHILD = textwrap.dedent(
    """
    import json, sys
    from office365.cli import _served

    line = _served("graph")
    imported = sorted({name.split(".")[1] for name in sys.modules if name.startswith("office365.")})
    print(json.dumps({"line": line, "imported": imported}))
    """
)


def _answer() -> dict:
    finished = subprocess.run([sys.executable, "-c", CHILD], capture_output=True, text=True, check=True)
    return json.loads(finished.stdout)


def test_the_product_list_is_read_from_the_index_without_importing_a_product() -> None:
    from office365.cli import AUDIENCES
    from office365.routing import products

    answer = _answer()

    assert not [name for name in answer["imported"] if name in products()]
    served = [name for name in products() if name not in AUDIENCES]
    assert answer["line"] == f"graph serves {len(served)} products: " + ", ".join(served)
