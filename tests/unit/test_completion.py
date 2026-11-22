"""The words a shell may offer: read off the model once, then read from the cache.

What is being pinned is the answer, not the implementation: a noun answers the commands of a
route before the links it holds, a line that ends on an action answers ``None`` (because the
flags there are a signature, not a word), and a warm node is served without asking the model
again. Completion never sends a request, so every one of these is a level-0 or level-1 answer.
"""

import json

import pytest
from office365 import completion


@pytest.fixture(autouse=True)
def _private_cache(tmp_path, monkeypatch):
    """Keep the developer's own completion cache, and an earlier test's, out of the test."""
    monkeypatch.setenv("O365_CACHE", str(tmp_path / "completion.json"))
    completion._document.cache_clear()


def test_a_noun_answers_the_commands_it_exposes_before_the_links_it_holds():
    node = completion.following("outlook", ("message",))

    kinds = [candidate.kind for candidate in node]
    assert kinds[0] == "action"
    assert kinds[kinds.index("navigation") - 1] == "action"
    assert "delete" in [candidate.word for candidate in node]
    assert "attachments" in [candidate.word for candidate in node]
    assert len({candidate.word for candidate in node}) == len(node)


def test_a_line_that_ends_on_an_action_answers_none_because_flags_are_a_signature():
    assert completion.following("outlook", ("message", "delete")) is None


def test_every_offered_word_is_a_word_the_router_would_accept():
    from office365.routing import route

    node = completion.following("outlook", ("message",))

    for candidate in node:
        assert route("outlook", "message", candidate.word) is not None


def test_a_warmed_node_is_served_without_building_it_again(monkeypatch):
    completion.warm(["outlook"])

    def _refuse(product, path):
        pytest.fail(f"built {product} {path}")

    monkeypatch.setattr(completion, "_build", _refuse)

    assert completion.following("outlook", ("message",)) is not None


def test_a_node_is_built_once_and_again_only_when_its_modules_have_changed(monkeypatch):
    completion.following("outlook", ("message",))
    built = []
    monkeypatch.setattr(completion, "_build", lambda product, path: built.append(path) or ())

    completion.following("outlook", ("message",))
    assert built == []

    document = json.loads(completion.cache_path().read_text("utf-8"))
    document["stamps"]["outlook"] = {"office365/outlook/mail/messages/message.py": 1}
    completion.cache_path().write_text(json.dumps(document), "utf-8")
    completion._document.cache_clear()  # forget this process's copy, as the next TAB would be

    completion.following("outlook", ("message",))
    assert built == [("message",)]


def test_the_command_line_answers_its_own_words_before_asking_the_model():
    from office365.cli import SESSION, _following

    top = [word for word, _ in _following([], "")]

    assert set(SESSION) <= set(top)
    assert "completion" in top
    assert _following(["nonsense"], "") == []


def test_the_doctor_page_offers_the_route_words_the_command_would_take():
    from office365.cli import _following

    assert "intune" in [word for word, _ in _following(["doctor"], "i")]
    assert "managed-device" in [word for word, _ in _following(["doctor", "intune"], "managed")]


def test_the_script_asks_the_hidden_command_and_no_user_facing_word():
    written = completion.script("bash")

    assert "__complete" in written
    assert "--prefix" in written
    with pytest.raises(LookupError, match="no completion script for 'tcsh'"):
        completion.script("tcsh")


def test_a_command_offers_only_the_formats_it_accepts():
    """A TAB that answered ``csv`` for ``doctor`` would hand back a word argparse refuses."""
    from office365.cli import DOCTOR_FORMATS, LICENCE_FORMATS, _following

    doctor = _following(["doctor", "-o"], "")
    licences = _following(["licences", "-o"], "")

    assert [word for word, _ in doctor] == list(DOCTOR_FORMATS)
    assert [word for word, _ in licences] == list(LICENCE_FORMATS)
    assert all(told for _, told in doctor)
