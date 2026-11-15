"""The shipped index is a render, not a file someone kept up to date.

``office365/index.json`` answers the questions a command line asks before it imports anything, so
if it drifts from the model the answers are wrong in the most misleading way available: they stay
plausible. The test builds the document again and compares bytes, which covers every rule the
writer states at once -- sorted products and nouns, sorted lists inside a record, the version
stamp, one line per noun.

The second test is about meaning rather than freshness: ``walks`` is read by the command line to
decide what it may advertise, so the two halves it keeps apart - the item a read wants and the
feed a listing wants - are pinned on a noun that has only one of them each.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

from generator.tools.index import DEFAULT_PATH, build_index, write_index

REPO_ROOT = Path(__file__).resolve().parents[2]


@lru_cache(maxsize=1)
def _built() -> Dict[str, Any]:
    """The document for the tree as it is now: 5 s of imports, read once for both tests."""
    return build_index()


def test_the_shipped_index_is_a_byte_identical_render(tmp_path: Path) -> None:
    rendered = write_index(tmp_path / "index.json", _built())

    assert rendered.read_bytes() == (REPO_ROOT / DEFAULT_PATH).read_bytes()


def test_a_noun_states_which_half_a_walk_lands_on() -> None:
    outlook = _built()["products"]["outlook"]["message"]

    assert outlook["walks"] == {"GraphClient": {"feed": ["me", "messages"]}}
    assert outlook["collection"] == "office365.outlook.mail.messages.collection:MessageCollection"
    assert "send" in outlook["verbs"]
    assert outlook["navigations"]["attachments"].endswith(":AttachmentCollection")
