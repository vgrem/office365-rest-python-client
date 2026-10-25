"""The user-profile reader answers properties by name, not by ordinal (offline).

``GetUserProfileProperties`` returns a CSOM property bag keyed by position --
``{"0": {"Key": "0|AboutMe", "Value": "", "ValueType": "Edm.String"}, ...}``. Read
literally, that is a dictionary of ``"0".."114"`` whose values are triples, so a caller
could not ask for ``AboutMe`` at all. The names are in the payload; the reader hands them
out, typed by ``ValueType``.
"""

from __future__ import annotations

from office365.runtime.converters.keyvalue import parse_key_value
from office365.sharepoint.client_context import ClientContext
from tests import test_site_url
from tests._scripted_transport import ScriptedTransport

_BAG = {
    "0": {"Key": "0|UserProfile_GUID", "Value": "8b44de87-f8bf-4987-99f0", "ValueType": "Edm.Guid"},
    "1": {"Key": "0|AboutMe", "Value": "", "ValueType": "Edm.String"},
    "2": {"Key": "0|Skills", "Value": "Python", "ValueType": "Edm.String"},
    "3": {"Key": "0|IsAdmin", "Value": "true", "ValueType": "Edm.Boolean"},
}


def _ctx(bag):
    ctx = ClientContext(test_site_url)
    ctx.pending_request().beforeExecute.clear()
    ctx.pending_request().transport = ScriptedTransport([{"d": bag}])
    return ctx


def test_a_profile_property_is_read_by_its_name():
    ctx = _ctx(_BAG)

    result = ctx.people_manager.get_user_profile_properties("i:0#.f|membership|mdoe@contoso.com").execute_query()

    # The ordinal prefix is the endpoint's, not the property's, and ``ValueType`` still types it.
    assert result.value == {
        "UserProfile_GUID": "8b44de87-f8bf-4987-99f0",
        "AboutMe": "",
        "Skills": "Python",
        "IsAdmin": True,
    }


def test_a_key_may_carry_an_ordinal_prefix():
    assert parse_key_value({"Key": "0|Skills", "Value": "Python", "ValueType": "Edm.String"}) == ("Skills", "Python")
    # A plainly keyed bag -- ``PersonProperties.UserProfileProperties`` -- is untouched.
    assert parse_key_value({"Key": "Skills", "Value": "Python", "ValueType": "Edm.String"}) == ("Skills", "Python")
