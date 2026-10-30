"""The location of a sign-in is the ``location`` member, not the status one.

``SignIn.location`` read ``status`` and answered a fresh ``SignInLocation`` whatever
the payload carried, so a sign-in that named its city, state and country appeared to
have none -- and ``_schema.properties["status"].attr`` named whichever getter of that
wire name came last in the class body.
"""

from __future__ import annotations

from office365.directory.audit.signins.location import SignInLocation
from office365.directory.audit.signins.signin import SignIn
from office365.migration.offline import offline_context


def test_the_location_getter_reads_the_location_member() -> None:
    sign_in = SignIn(offline_context())
    location = SignInLocation()
    sign_in.set_property("location", location)

    assert sign_in.location is location
