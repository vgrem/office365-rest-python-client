"""Offline tests for ``Web.get_securable_object`` and the ``grant_access``/``revoke_access`` wrappers.

``get_securable_object`` is a pure address builder (deferred, no request), so the
bulk of these tests assert the resource path it produces. The permission helpers
are checked by driving a scripted transport and inspecting the request sent.
"""

from __future__ import annotations

import pytest
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.listitem import ListItem
from office365.sharepoint.lists.list import List
from office365.sharepoint.permissions.roles.definitions.definition import RoleDefinition
from office365.sharepoint.permissions.securable_object import SecurableObject
from office365.sharepoint.principal.users.user import User
from tests import test_site_url
from tests._scripted_transport import ScriptedTransport


class _CaptureTransport(ScriptedTransport):
    def __init__(self, payloads):
        super().__init__(payloads)
        self.requests = []

    def execute(self, request):
        self.requests.append(request)
        return super().execute(request)


PRINCIPAL_ID = 6
ROLE_DEF_ID = 1073741827


def _ctx() -> ClientContext:
    return ClientContext(test_site_url)


# --- Web.get_securable_object -------------------------------------------------


def test_scope_web_returns_the_web_itself():
    ctx = _ctx()

    assert ctx.web.get_securable_object("web") is ctx.web


def test_scope_site_is_an_alias_for_web():
    ctx = _ctx()

    assert ctx.web.get_securable_object("site") is ctx.web


def test_scope_is_case_insensitive():
    ctx = _ctx()

    assert ctx.web.get_securable_object("WEB") is ctx.web
    assert isinstance(ctx.web.get_securable_object("Folder", url="/sites/x/f"), ListItem)


def test_scope_list_returns_list_addressed_by_title():
    ctx = _ctx()

    target = ctx.web.get_securable_object("list", list_title="Documents")

    assert isinstance(target, List)
    assert isinstance(target, SecurableObject)
    assert "GetByTitle" in str(target.resource_path)
    assert "Documents" in str(target.resource_path)


def test_scope_list_requires_a_title():
    ctx = _ctx()

    with pytest.raises(ValueError, match="list_title"):
        ctx.web.get_securable_object("list")


def test_scope_folder_returns_the_folders_list_item():
    ctx = _ctx()
    path = "/sites/x/Shared Documents/sub"

    target = ctx.web.get_securable_object("folder", url=path)

    assert isinstance(target, ListItem)
    resource_path = str(target.resource_path)
    assert "getFolderByServerRelativePath" in resource_path
    assert "ListItemAllFields" in resource_path
    assert path in resource_path


def test_scope_folder_requires_a_url():
    ctx = _ctx()

    with pytest.raises(ValueError, match="url"):
        ctx.web.get_securable_object("folder")


def test_scope_item_returns_the_documents_list_item():
    ctx = _ctx()
    path = "/sites/x/Shared Documents/report.docx"

    target = ctx.web.get_securable_object("item", url=path)

    assert isinstance(target, ListItem)
    resource_path = str(target.resource_path)
    assert "getFileByServerRelativePath" in resource_path
    assert "listItemAllFields" in resource_path
    assert path in resource_path


def test_scope_file_is_an_alias_for_item():
    ctx = _ctx()

    target = ctx.web.get_securable_object("file", url="/sites/x/Shared Documents/report.docx")

    assert isinstance(target, ListItem)
    assert "getFileByServerRelativePath" in str(target.resource_path)


def test_scope_item_requires_a_url():
    ctx = _ctx()

    with pytest.raises(ValueError, match="url"):
        ctx.web.get_securable_object("item")


def test_unknown_scope_raises():
    ctx = _ctx()

    with pytest.raises(ValueError, match="Unsupported scope"):
        ctx.web.get_securable_object("nope")


def test_non_string_scope_raises():
    ctx = _ctx()

    with pytest.raises(ValueError, match="Unsupported scope"):
        ctx.web.get_securable_object(None)  # type: ignore[arg-type]


def test_resolution_is_deferred():
    """Addressing a securable object must not queue a request."""
    ctx = _ctx()
    ctx.pending_request().beforeExecute.clear()

    ctx.web.get_securable_object("folder", url="/sites/x/Shared Documents/sub")

    assert not ctx._queries


# --- SecurableObject.grant_access / revoke_access -----------------------------


def _grant_ctx(payloads):
    ctx = _ctx()
    ctx.pending_request().beforeExecute.clear()
    transport = _CaptureTransport(payloads)
    ctx.pending_request().transport = transport
    return ctx, transport


def _loaded_principal(ctx) -> User:
    principal = User(ctx)
    principal.set_property("Id", PRINCIPAL_ID)
    return principal


def _loaded_role(ctx) -> RoleDefinition:
    role = RoleDefinition(ctx)
    role.set_property("Id", ROLE_DEF_ID)
    return role


def test_grant_access_queues_add_role_assignment():
    ctx, transport = _grant_ctx([{}])
    target = ctx.web.get_securable_object("list", list_title="Documents")

    result = target.grant_access(_loaded_principal(ctx), _loaded_role(ctx)).execute_query()

    assert result is target
    assert len(transport.requests) == 1
    request = transport.requests[0]
    assert "AddRoleAssignment" in request.url
    assert f"principalId={PRINCIPAL_ID}" in request.url
    assert f"roleDefId={ROLE_DEF_ID}" in request.url


def test_revoke_access_queues_remove_role_assignment():
    ctx, transport = _grant_ctx([{}])
    target = ctx.web.get_securable_object("list", list_title="Documents")

    result = target.revoke_access(_loaded_principal(ctx), _loaded_role(ctx)).execute_query()

    assert result is target
    assert len(transport.requests) == 1
    assert "RemoveRoleAssignment" in transport.requests[0].url


def test_grant_access_is_deferred():
    ctx = _ctx()
    ctx.pending_request().beforeExecute.clear()
    transport = _CaptureTransport([])
    ctx.pending_request().transport = transport
    target = ctx.web.get_securable_object("web")

    target.grant_access(_loaded_principal(ctx), _loaded_role(ctx))

    assert transport.calls == 0
    assert transport.requests == []
