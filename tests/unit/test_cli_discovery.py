"""The level-0 answer is read, not imported.

``o365 graph`` says what one token serves. Answering it by importing the tree costs 5.2 s; the
index the generator ships holds the same list, so the command parses a file (4 ms) and imports
nothing. The test runs the command in a child process, because in this one every package has been
imported by some other test already: what it can assert is the import set of a fresh interpreter.
"""

from __future__ import annotations

import json
import os
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


#: ``doctor`` answers for the whole library, so the same rule holds twice over: it names every
#: product, and importing them all is what it must not do. Run in a child with no session, both
#: halves are read - the index and the empty store - and nothing is called. The report module is
#: imported before the snapshot because it is the page's own vocabulary: it reaches a constants
#: module that happens to live in a product package, which says nothing about this command.
DOCTOR = textwrap.dedent(
    """
    import contextlib, io, json, sys
    from office365.cli import main
    from office365.licensing.report import of  # noqa: F401 - the doctor's own vocabulary

    before = set(sys.modules)
    with contextlib.redirect_stdout(io.StringIO()):
        code = main(["doctor", "-o", "json"])
    imported = sorted({name.split(".")[1] for name in set(sys.modules) - before if name.startswith("office365.")})
    print(json.dumps({"code": code, "imported": imported}))
    """
)


def _answer() -> dict:
    finished = subprocess.run([sys.executable, "-c", CHILD], capture_output=True, text=True, check=True)
    return json.loads(finished.stdout)


def _doctor(tmp_path) -> dict:
    finished = subprocess.run(
        [sys.executable, "-c", DOCTOR],
        capture_output=True,
        text=True,
        check=True,
        env={**os.environ, "O365_HOME": str(tmp_path)},
    )
    return json.loads(finished.stdout)


def test_doctor_answers_for_every_product_without_importing_one(tmp_path) -> None:
    from office365.routing import products

    answer = _doctor(tmp_path)

    assert answer["code"] == 0
    assert not [name for name in answer["imported"] if name in products()]


def test_the_product_list_is_read_from_the_index_without_importing_a_product() -> None:
    from office365.cli import AUDIENCES
    from office365.routing import products

    answer = _answer()

    assert not [name for name in answer["imported"] if name in products()]
    served = [name for name in products() if name not in AUDIENCES]
    assert answer["line"] == f"graph serves {len(served)} products: " + ", ".join(served)
