"""What a login says, and what a report says: a greeting is not a listing.

The two read the same kept claims through one decode. The difference the tests pin is the one a
person feels: a login counts the grants and points at the words that name them, because the
moment you have just signed in is the wrong moment to read seventy scope names.
"""

import time

from office365 import cli


def _entry(grants="Mail.Read Write User.Read", **claims):
    return {
        "mode": "device-flow",
        "claims": {
            "preferred_username": "vadimadm@mediadev8.onmicrosoft.com",
            "tid": "af6a80a4-8b4b-4879-88af-42ff8a545211",
            "scp": grants,
            "exp": int(time.time()) + 3900,
            **claims,
        },
    }


def test_a_login_counts_the_grants_and_points_at_the_words_that_name_them():
    welcome = cli._welcome("graph", _entry())

    assert "logged in: graph as vadimadm@mediadev8.onmicrosoft.com" in welcome
    assert "3 permissions" in welcome
    assert "Mail.Read" not in welcome
    assert "o365 whoami" in welcome and "o365 doctor" in welcome


def test_a_report_names_the_grants_because_that_is_the_question_it_answers():
    summary = cli._summary("graph", _entry())

    assert "grants: Mail.Read Write User.Read" in summary
    assert "mode device-flow, 1 h left" in summary


def test_a_token_with_no_scope_says_so_rather_than_counting_zero():
    welcome = cli._welcome("exchange", _entry(grants=""))

    assert "no permissions" in welcome


def test_an_expired_token_says_how_long_ago_and_leaves_the_fix_to_the_doctor():
    """The fact belongs to the row, the command to the verdict: said twice it reads as two faults."""
    expired = _entry(exp=int(time.time()) - 60)

    summary = cli._summary("graph", expired)

    assert "expired 1 min ago" in summary
    assert "fetching" not in summary and "run o365" not in summary


def test_a_session_left_alone_for_days_is_not_counted_in_minutes():
    stale = _entry(exp=int(time.time()) - 3 * 24 * 3600 - 60)

    assert "expired 3 d ago" in cli._summary("graph", stale)
