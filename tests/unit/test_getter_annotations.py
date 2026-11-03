"""A column's declared type decides how a wire value is coerced.

``declared_type`` evaluates the getter's return annotation, so an annotation the runtime
cannot see leaves the column holding whatever the service sent. These are the two value
facts that costs: an enum column keeps the member, and a member the snapshot does not
list is kept as sent rather than coerced to ``None``.
"""

from __future__ import annotations

from office365.admin.browser_shared_cookie import BrowserSharedCookie
from office365.intune.browser.sharedcookiesourceenvironment import BrowserSharedCookieSourceEnvironment
from office365.onedrive.operations.long_running import LongRunningOperation
from office365.onedrive.operations.longrunningoperationstatus import LongRunningOperationStatus
from office365.runtime.converters.value import declared_type


def test_an_enum_column_holds_the_member_not_the_wire_string() -> None:
    # The metadata spells the ordinal ("2") and ``both`` is the member it names.
    cookie = BrowserSharedCookie(None)
    cookie.set_property("sourceEnvironment", "2")

    assert cookie.source_environment is BrowserSharedCookieSourceEnvironment.both
    assert declared_type(BrowserSharedCookie, "sourceEnvironment") is BrowserSharedCookieSourceEnvironment


def test_an_unfamiliar_enum_value_is_kept_as_the_service_sent_it() -> None:
    # A member the snapshot does not list (the engine's "completed", where the entity
    # enum says "succeeded") must not be coerced to None: the next update would write
    # null back over a value the service reported.
    operation = LongRunningOperation(None)

    operation.set_property("status", "completed")
    assert operation.properties["status"] == "completed"

    operation.set_property("status", "succeeded")
    assert operation.status is LongRunningOperationStatus.succeeded
