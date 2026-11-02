"""An empty nested value is not sent, and a populated one still is.

SharePoint 2019 refuses a payload that carries a field its type does not know:

    Microsoft.Data.OData.ODataException: property CoAuthState does not exist on type
    SP.Publishing.SitePageFieldsData. Use only property names defined by the type.

The name *is* defined by the type on a modern farm, so the defect was not the field: it was
that ``SitePageFieldsData`` holds four ``default_factory`` values, and serialising every
attribute sent ``"CoAuthState": {}`` — an empty object where the type wants an object it can
read. ``ClientValue.to_json`` now omits a nested value with nothing to send, recursively, so
a payload carries only what the caller filled in.
"""

from office365.sharepoint.publishing.pages.coauth_state import SitePageCoAuthState
from office365.sharepoint.publishing.pages.fields_data import SitePageFieldsData


def test_an_all_default_value_serialises_only_what_was_set():
    # Four default_factory members (AuthoringMetadata, BoostProperties, CoAuthState and an
    # empty collection) must contribute nothing; only the title the caller passed is sent.
    assert SitePageFieldsData(Title="x").to_json() == {"Title": "x"}


def test_an_emptied_value_serialises_to_nothing():
    assert SitePageCoAuthState().to_json() == {}


def test_a_populated_nested_value_is_still_sent():
    payload = SitePageFieldsData(Title="x", CoAuthState=SitePageCoAuthState(IsNewSession=True)).to_json()

    # CoAuthState survives because one of *its* members is set; its own empty collection is
    # still dropped, and its empty sibling values stay out of the payload altogether.
    assert payload == {"Title": "x", "CoAuthState": {"IsNewSession": True}}


def test_the_rule_holds_in_both_directions():
    value = SitePageFieldsData().hydrate({"Title": "x", "CoAuthState": {"IsNewSession": True}})

    assert value.CoAuthState.IsNewSession is True
    assert value.to_json() == {"Title": "x", "CoAuthState": {"IsNewSession": True}}
