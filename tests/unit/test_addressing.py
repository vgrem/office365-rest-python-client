"""How a request names the thing it acts on: the path, the key, the query string, the ask.

A caller says *which* resource four ways, and each one has exactly one owner. The path is built
from a parent plus a segment; the key is declared above the class and read from
``TypeSchema.key``; the query string is written the way the specification spells it; and
``Prefer`` states what the answer should look like. All four are pure: nothing here needs a
tenant, which is why they can be pinned to the character.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime, timezone
from typing import Optional

import pytest
from office365.entity import Entity
from office365.graph_client import GraphClient
from office365.migration.offline import offline_sharepoint_context
from office365.onedrive.internal.paths.url import UrlPath
from office365.runtime.http.prefer import (
    BYPASS_SHARED_LOCK,
    RESPOND_ASYNC,
    RETURN_REPRESENTATION,
    add_prefer,
    prefer_create_if_missing,
    prefer_return_representation,
)
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.odata.literals import odata_literal
from office365.runtime.odata.query_options import QueryOptions
from office365.runtime.paths.alternate_key import AlternateKeyPath
from office365.runtime.paths.appid import AppIdPath
from office365.runtime.paths.builder import ODataPathBuilder
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import CompositeKeyNotSupported, key, odata
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.entity import Entity as SharePointEntity
from office365.sharepoint.webs.web import Web
from tests import test_site_url

# --- the path a request is addressed at -----------------------------------------------


def test_a_url_path_reaches_a_drive_item_and_a_term():
    client = GraphClient()
    parent = client.me.drive.root.resource_path
    assert parent is not None
    path = UrlPath("Sample.docx", UrlPath("2018", UrlPath("archive", parent)))
    item_id = uuid.uuid4().hex
    path = path.set_segment(item_id)
    assert str(path) == f"/me/drive/items/{item_id}"

    group_id, set_id, term_id = uuid.uuid4().hex, uuid.uuid4().hex, uuid.uuid4().hex
    terms = client.sites.root.term_store.groups[group_id].sets[set_id].children.resource_path
    assert terms is not None
    assert str(terms.set_segment(term_id)) == f"/sites/root/termStore/groups/{group_id}/sets/{set_id}/terms/{term_id}"


def test_an_entity_method_path_survives_an_id_mapping():
    # A pre-existing service-operation path (GetByTitle) must not be clobbered by an Id.
    lst = ClientContext(test_site_url).web.lists.get_by_title("X")
    lst.set_property("Id", 6)
    assert "GetByTitle" in str(lst.resource_path)


def test_a_web_addresses_itself_at_web_not_at_the_collection_it_came_from():
    """A web's OData segment is ``Web``; a subweb's address is its own ``Url``.

    Both halves are one fact: a ``Web`` reached through ``web.webs`` is still the same
    endpoint, and once the service reports ``Url`` the object addresses that site rather than
    the site it was listed from. A ``$select`` that omits ``Url`` leaves the first half in
    place, which is why it must not be a URL derived from the parent collection.
    """
    ctx = offline_sharepoint_context()
    assert str(Web(ctx).resource_path) == "/Web"
    assert str(ctx.web.webs.create_typed_object().resource_path) == "/Web"

    web = Web(ctx)
    web.set_property("Url", "https://contoso.sharepoint.com/sites/other")
    assert web.resource_url == "https://contoso.sharepoint.com/sites/other/_api/Web"


def test_a_function_argument_is_an_odata_literal():
    """A ``datetime`` argument used to fall through to ``quote(str(value))``.

    That produced an invalid path (e.g. for ``TimeZone.UTCToLocalTime``), so the argument now
    leaves as the literal its type declares -- and a UTC mark is dropped, because the v3
    spelling has nowhere to put it.
    """
    assert ODataPathBuilder._encode_odata_value(datetime(2021, 6, 1, 15, 0, 0)) == "datetime'2021-06-01T15:00:00'"
    assert (
        ODataPathBuilder._encode_odata_value(datetime(2021, 6, 1, 15, 0, 0, tzinfo=timezone.utc))
        == "datetime'2021-06-01T15:00:00'"
    )
    assert ODataPathBuilder._encode_odata_value(date(2021, 6, 1)) == "date'2021-06-01'"


def test_an_odata_literal_is_a_literal_not_a_url():
    assert odata_literal(42) == "42"
    assert odata_literal(True) == "true"
    assert odata_literal(False) == "false"
    assert odata_literal(None) == "null"
    # Slashes stay literal inside a string literal (no %2F URL inflation).
    path = "/sites/x/Shared Documents/deep/nested/folder/report.xlsx"
    resource_path = ClientContext(test_site_url).web.get_file_by_server_relative_path(path).resource_path
    assert "%2F" not in str(resource_path)
    assert path in str(resource_path)


def test_an_alternate_key_is_addressed_by_name():
    app_id = "00000000-0000-0000-0000-000000000000"
    path = AppIdPath(app_id, ResourcePath("servicePrincipals"))
    assert isinstance(path, AlternateKeyPath)
    assert path.key_name == "appId"
    assert str(path) == f"/servicePrincipals(appId='{app_id}')"


# --- the key a type declares ----------------------------------------------------------


@key("tenantId")
class _Partner(Entity):
    @odata(name="tenantId")
    @property
    def tenant_id(self) -> Optional[str]:
        return self.properties.get("tenantId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Partner"


class _Inheriting(_Partner):
    """A derived type inherits the key, exactly as it inherits the declared property."""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.InheritingPartner"


def test_a_type_with_no_declaration_answers_its_family_default():
    class _Plain(Entity):
        @property
        def entity_type_name(self) -> str:
            return "microsoft.graph.Plain"

    class _PlainItem(SharePointEntity):
        @property
        def entity_type_name(self) -> str:
            return "SP.PlainItem"

    assert _Plain._schema.key == "id"
    assert _PlainItem._schema.key == "Id"


def test_a_declared_key_is_inherited_and_reaches_both_readers():
    """The decorator sits above a class whose schema was built already, so it rebuilds it."""
    for owner in (_Partner, _Partner(GraphClient()), _Inheriting, _Inheriting(GraphClient())):
        assert owner._schema.key == "tenantId"


def test_only_the_declared_key_re_anchors_the_path():
    """What ``set_property`` asks: only the key re-anchors, and only under its own name."""
    entity = _Partner(GraphClient())
    entity.set_property("tenantId", "contoso")
    assert str(entity.resource_path) == "/contoso"

    plain = Entity(GraphClient())
    plain.set_property("id", "123")
    assert str(plain.resource_path) == "/123"

    # Setting ``id`` on a type whose identity is ``tenantId`` must not move the path.
    other = _Partner(GraphClient())
    other.set_property("id", "123")
    assert other.resource_path is None


def test_the_identity_is_fetched_with_the_properties():
    """What ``ensure_properties`` asks: a read asks for the key, so the path can be rebuilt."""
    client = GraphClient()
    _Partner(client).ensure_properties(["displayName"])
    assert client._queries[-1].query_options.select == ["displayName", "tenantId"]

    plain = Entity(client)
    plain.ensure_properties(["displayName"])
    assert client._queries[-1].query_options.select == ["displayName", "id"]


def test_a_composite_key_is_refused_rather_than_half_supported():
    with pytest.raises(CompositeKeyNotSupported, match="appId/tenantId"):

        @key("appId", "tenantId")
        class _Composite(Entity):
            pass


def test_a_key_naming_nothing_clears_the_inherited_one():
    """A folder is reached by its path, so an ``Id`` it is handed must not re-anchor it."""

    @key()
    class _Unkeyed(SharePointEntity):
        @property
        def entity_type_name(self) -> str:
            return "SP.Folder"

    assert _Unkeyed._schema.key == ""
    entity = _Unkeyed(GraphClient())
    entity.set_property("Id", "7e1c")
    assert entity.resource_path is None


# --- the query string ----------------------------------------------------------------


def test_a_standard_option_is_spelled_the_way_the_specification_spells_it():
    options = QueryOptions(select=["subject"], filter="isRead eq false", order_by="receivedDateTime asc", top=5, skip=10)
    assert options.to_url() == ("$select=subject&$filter=isRead eq false&$orderby=receivedDateTime asc&$top=5&$skip=10")


def test_a_custom_key_is_emitted_as_the_caller_spelled_it():
    options = QueryOptions(custom={"token": "latest", "$orderby": "id desc"})
    assert options.to_url() == "token=latest&$orderby=id desc"


# --- what a request asks the service to prefer ---------------------------------------


def _request(prefer: str | None = None) -> RequestOptions:
    request = RequestOptions("https://graph.microsoft.com/v1.0/me")
    if prefer is not None:
        request.set_header("Prefer", prefer)
    return request


def test_two_preferences_are_comma_joined_in_order():
    request = _request()
    prefer_create_if_missing(request)
    prefer_return_representation(request)
    assert request.headers["Prefer"] == f"create-if-missing, {RETURN_REPRESENTATION}"


def test_a_value_already_present_is_not_duplicated():
    request = _request(f"{BYPASS_SHARED_LOCK}, {RESPOND_ASYNC}")
    add_prefer(request, RESPOND_ASYNC, RETURN_REPRESENTATION)
    assert request.headers["Prefer"] == f"{BYPASS_SHARED_LOCK}, {RESPOND_ASYNC}, {RETURN_REPRESENTATION}"


def test_nothing_is_attached_when_no_value_is_given():
    request = _request()
    add_prefer(request, "")
    assert "Prefer" not in request.headers
