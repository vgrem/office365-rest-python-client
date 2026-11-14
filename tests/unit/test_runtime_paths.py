"""Where a request is addressed: path segments, alternate keys, and OData literals."""

from __future__ import annotations

import unittest
import uuid

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
from office365.runtime.paths.builder import ODataPathBuilder
from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.client_context import ClientContext
from tests import test_site_url


class TestGraphPathBuilding(unittest.TestCase):
    """Building and resolving Graph resource paths is a pure in-memory operation."""

    client = GraphClient()

    def test_resolve_drive_url_path(self):
        parent_path = self.client.me.drive.root.resource_path
        assert parent_path is not None
        path = UrlPath("Sample.docx", UrlPath("2018", UrlPath("archive", parent_path)))
        item_id = uuid.uuid4().hex
        path.set_segment(item_id)
        self.assertEqual(f"/me/drive/items/{item_id}", str(path))

    def test_resolve_term_children_path(self):
        group_id = uuid.uuid4().hex
        set_id = uuid.uuid4().hex
        term_id = uuid.uuid4().hex
        path = self.client.sites.root.term_store.groups[group_id].sets[set_id].children.resource_path
        assert path is not None
        path = path.set_segment(term_id)
        self.assertEqual(
            f"/sites/root/termStore/groups/{group_id}/sets/{set_id}/terms/{term_id}",
            str(path),
        )


def test_odata_literal_emits_numbers_booleans_and_null_bare():
    assert odata_literal(42) == "42"
    assert odata_literal(True) == "true"
    assert odata_literal(False) == "false"
    assert odata_literal(None) == "null"


def test_entity_method_path_is_not_clobbered_by_id():
    """A pre-existing service-operation path (GetByTitle) must survive an Id mapping."""
    ctx = ClientContext(test_site_url)
    lst = ctx.web.lists.get_by_title("X")

    lst.set_property("Id", 6)

    assert "GetByTitle" in str(lst.resource_path)


def test_odata_literal_keeps_slashes():
    """Slashes stay literal in OData string literals (no %2F URL inflation)."""
    ctx = ClientContext(test_site_url)
    path = "/sites/x/Shared Documents/deep/nested/folder/report.xlsx"

    resource_path = ctx.web.get_file_by_server_relative_path(path).resource_path

    assert "%2F" not in str(resource_path)
    assert path in str(resource_path)


def test_odata_function_datetime_argument_uses_datetime_literal():
    """A datetime function argument becomes an OData v3 ``datetime'...'`` literal.

    Before this branch a ``datetime`` fell through to ``quote(str(value))``, which
    produced an invalid path (e.g. for ``TimeZone.UTCToLocalTime``).
    """
    from datetime import date, datetime, timezone

    assert ODataPathBuilder._encode_odata_value(datetime(2021, 6, 1, 15, 0, 0)) == "datetime'2021-06-01T15:00:00'"
    assert (
        ODataPathBuilder._encode_odata_value(datetime(2021, 6, 1, 15, 0, 0, tzinfo=timezone.utc))
        == "datetime'2021-06-01T15:00:00'"
    )
    assert ODataPathBuilder._encode_odata_value(date(2021, 6, 1)) == "date'2021-06-01'"


def test_appid_path_is_an_alternate_key_path():
    from office365.runtime.paths.alternate_key import AlternateKeyPath
    from office365.runtime.paths.appid import AppIdPath

    app_id = "00000000-0000-0000-0000-000000000000"
    path = AppIdPath(app_id, ResourcePath("servicePrincipals"))

    assert isinstance(path, AlternateKeyPath)
    assert path.key_name == "appId"
    assert str(path) == f"/servicePrincipals(appId='{app_id}')"


def test_a_web_addresses_itself_at_web_not_at_the_collection_it_came_from():
    """A web's OData segment is ``Web``; a subweb's address is its own ``Url``.

    Both halves are one fact: a ``Web`` reached through ``web.webs`` is still the same
    endpoint, and once the service reports ``Url`` the object addresses that site rather
    than the site it was listed from. A ``$select`` that omits ``Url`` leaves the first
    half in place, which is why it must not be a URL derived from the parent collection.
    """
    from office365.sharepoint.webs.web import Web

    ctx = offline_sharepoint_context()

    assert str(Web(ctx).resource_path) == "/Web"
    assert str(ctx.web.webs.create_typed_object().resource_path) == "/Web"

    web = Web(ctx)
    web.set_property("Url", "https://contoso.sharepoint.com/sites/other")
    assert web.resource_url == "https://contoso.sharepoint.com/sites/other/_api/Web"


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
