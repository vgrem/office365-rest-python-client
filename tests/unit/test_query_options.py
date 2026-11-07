"""What each query option is called in a request.

A misspelled option is not refused — the service answers ``200`` and drops it — so
the name is only visible in the URL, and there is nothing on the wire to observe.
These tests pin that spelling; that the service *honours* the ordering is a live
fact, pinned in ``tests/outlook/test_messages.py``.
"""

from office365.runtime.odata.query_options import QueryOptions


def test_a_standard_option_is_spelled_the_way_the_specification_spells_it():
    options = QueryOptions(
        select=["subject"],
        filter="isRead eq false",
        order_by="receivedDateTime asc",
        top=5,
        skip=10,
    )
    assert options.to_url() == ("$select=subject&$filter=isRead eq false&$orderby=receivedDateTime asc&$top=5&$skip=10")


def test_a_custom_key_is_emitted_as_the_caller_spelled_it():
    options = QueryOptions(custom={"token": "latest", "$orderby": "id desc"})
    assert options.to_url() == "token=latest&$orderby=id desc"
