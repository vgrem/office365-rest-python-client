"""One pin per defect a shipped version fixed.

Every test here guarded a specific way a value reached a user wrong: a getter reading a
neighbour's wire name, a body spelling a literal the service rejects, a helper dropping
part of what it was given. They live in one file so the pins stay cheap to read -- the
comment above each names the defect, the assertion names the outcome.
"""

from __future__ import annotations

import asyncio
import base64
import io
from datetime import datetime, timedelta, timezone

import pytest
import requests
from office365.directory.applications.data_type import ApplicationDataType
from office365.directory.audit.signins.location import SignInLocation
from office365.directory.audit.signins.signin import SignIn
from office365.directory.authentication.methods.modes import AuthenticationMethodModes
from office365.directory.credential import CredentialExpiryStatus
from office365.directory.key_credential import KeyCredential
from office365.directory.password_credential import PasswordCredential
from office365.directory.protection.threatassessment.requests.url import UrlAssessmentRequest
from office365.graph_client import GraphClient
from office365.intune.devices.and_app_management_role_assignment import DeviceAndAppManagementRoleAssignment
from office365.migration.map import ContentTypeMap
from office365.migration.offline import offline_context
from office365.migration.package.crypto import decrypt, encrypt, normalize_key
from office365.planner.tasks.task import PlannerTask
from office365.planner.tasks.task_details import PlannerTaskDetails
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.client_result import ClientResult
from office365.runtime.converters.keyvalue import parse_key_value
from office365.runtime.converters.scalars import parse_enum
from office365.runtime.converters.value import coerce_value
from office365.runtime.exceptions import AccessDeniedException, ObjectNotFoundException
from office365.runtime.http.prefer import (
    CREATE_IF_MISSING,
    RETURN_REPRESENTATION,
    prefer_create_if_missing,
    prefer_outlook_timezone,
    prefer_return_representation,
    prefer_upsert,
)
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.odata.v4.json_format import V4JsonFormat
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.verification import VerificationReport
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.contenttypes.fieldlinks.field_link import FieldLink
from office365.sharepoint.fields.field import Field
from office365.sharepoint.listitems.caml.guard import threshold_warnings, warn_if_unpaged
from office365.sharepoint.listitems.caml.query import CamlQuery
from office365.sharepoint.listitems.listitem import ListItem
from office365.sharepoint.publishing.pages.canvas import WEB_PART_CONTROL_TYPE, parse_canvas_controls
from office365.sharepoint.search.query.sort.sort import Sort
from office365.sharepoint.sharing.links.kind import SharingLinkKind
from office365.sharepoint.webhooks.subscription_information import SubscriptionInformation
from office365.teams.chats.collection import ChatCollection
from office365.teams.chats.type import ChatType
from office365.teams.messaging_settings import TeamMessagingSettings
from office365.teams.team import Team
from tests import test_site_url
from tests._scripted_transport import RecordingTransport, RoutingTransport, ScriptedTransport


def _context(payloads) -> ClientContext:
    ctx = ClientContext(test_site_url)
    ctx.pending_request().beforeExecute.clear()
    ctx.pending_request().transport = ScriptedTransport(payloads)
    return ctx


def _graph(payloads) -> GraphClient:
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = ScriptedTransport(payloads)
    return client


# --- a getter that read a neighbour's wire name -------------------------------------


def test_the_sign_in_location_is_the_location_member():
    # ``SignIn.location`` read ``status``, so every sign-in looked like it had no city.
    sign_in = SignIn(offline_context())
    location = SignInLocation()
    sign_in.set_property("location", location)
    assert sign_in.location is location


def test_the_team_messaging_settings_read_their_own_member():
    # ``Team.messaging_settings`` read ``guestSettings`` and answered an empty value.
    team = Team(offline_context())
    messaging = TeamMessagingSettings()
    team.set_property("messagingSettings", messaging)
    assert team.messaging_settings is messaging


def test_a_field_link_wears_the_internal_name_it_is_given():
    # ``field_internal_name`` answered ``Name`` even when ``FieldInternalName`` was set.
    link = FieldLink(ClientContext(test_site_url))
    link.set_property("Name", "Title")
    link.set_property("FieldInternalName", "Custom")
    assert link.field_internal_name == "Custom"


def test_a_chat_created_with_members_still_navigates_by_its_id():
    # The members navigation was cached against a parentless path and kept resolving to
    # ``/members`` after the create response assigned the id.
    chats = ChatCollection(GraphClient(tenant="contoso.onmicrosoft.com"), ResourcePath("chats"))
    chat = chats.add(ChatType.oneOnOne, owner_ids=["owner-1", "owner-2"])
    chat.set_property("id", "19:abc@unq.gbl.spaces")

    assert chat.members.resource_path.to_url() == "/chats/19:abc@unq.gbl.spaces/members"
    assert chat.messages.resource_path.to_url() == "/chats/19:abc@unq.gbl.spaces/messages"


def test_the_intune_role_assignment_keeps_its_odata_type():
    assignment = DeviceAndAppManagementRoleAssignment(None)
    assert assignment.entity_type_name == "microsoft.graph.deviceAndAppManagementRoleAssignment"
    assert list(assignment.members) == []


def test_ensure_indexed_queues_the_enable_and_leaves_the_column_to_the_server():
    ctx = ClientContext(test_site_url)
    field = Field(ctx)
    field.set_property("Indexed", False)
    field.ensure_indexed()

    assert len(ctx._queries) == 1
    assert field.properties["Indexed"] is False


def test_a_url_assessment_advertises_its_concrete_type():
    # The abstract base type is rejected by the service with ``InvalidBody``.
    request = UrlAssessmentRequest(GraphClient())
    request.set_property("url", "http://test-phishing-example.com")
    payload = request.to_json(V4JsonFormat())

    assert payload["@odata.type"] == "#microsoft.graph.urlAssessmentRequest"
    assert payload["url"] == "http://test-phishing-example.com"


# --- a body that spelled a value the service rejects --------------------------------


def _share_request(item: ListItem, **kwargs):
    item.share_link(SharingLinkKind.AnonymousView, **kwargs)
    return item.context.queries[-1]._parameters_type["request"]


class _FakeContext:
    def __init__(self) -> None:
        self.queries = []

    def add_query(self, query) -> None:
        self.queries.append(query)


def test_a_share_link_expiration_is_utc_with_z():
    # The literal carried microseconds and ``+00:00``; the service takes neither.
    item = ListItem(_FakeContext())
    request = _share_request(item, expiration=datetime(2026, 1, 1, 0, 0, 0, 123456, tzinfo=timezone.utc))
    assert request.to_json()["settings"]["expiration"] == "2026-01-01T00:00:00Z"


def test_a_share_link_without_an_expiration_omits_the_member():
    item = ListItem(_FakeContext())
    assert "expiration" not in _share_request(item).to_json()["settings"]


def test_a_subscription_expiration_is_utc_with_z():
    info = SubscriptionInformation(
        notificationUrl="https://example.com/hook",
        resource="resource",
        expirationDateTime=datetime(2026, 1, 1, 12, 0, 0, 123456, tzinfo=timezone.utc),
    )
    assert info.to_json()["expirationDateTime"] == "2026-01-01T12:00:00Z"


def test_a_graph_subscription_accepts_a_resource_path():
    # ``subscriptions.add`` spelled the path object into the body instead of its url.
    client = GraphClient(tenant="contoso.onmicrosoft.com")
    client.subscriptions.add(
        change_type="updated",
        notification_url="https://example.com/hook",
        resource=ResourcePath("me/drive/root"),
        expiration=datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
    )
    assert client._queries[-1]._parameters_type["resource"] == "me/drive/root"


def test_a_posted_search_query_carries_its_sort_list():
    # The POST form spells the sort as ``SortList``, not ``sortList``, and each entry
    # declares its own metadata type.
    transport = RoutingTransport([("postquery", {})])
    ctx = ClientContext(test_site_url)
    ctx.pending_request().beforeExecute.clear()
    ctx.pending_request().transport = transport

    ctx.search.post_query(
        "contoso",
        select_properties=["Title"],
        enable_sorting=True,
        sort_list=[Sort(Direction=0, Property="Modified")],
    ).execute_query()

    body = transport.requests[0].data["request"]
    assert body["SortList"]["results"] == [
        {"Direction": 0, "Property": "Modified", "__metadata": {"type": "Microsoft.SharePoint.Client.Search.Query.Sort"}}
    ]
    assert body["SortList"]["__metadata"]["type"] == "Collection(Microsoft.SharePoint.Client.Search.Query.Sort)"


def test_a_created_page_sends_bytes_and_named_attachments():
    # ``add`` wrapped a ``str`` presentation in ``BytesIO`` and typed every attachment
    # ``application/octet-stream``, whatever the file said it was.
    class _Recording(ScriptedTransport):
        def __init__(self, payloads):
            super().__init__(payloads)
            self.requests = []

        def execute(self, request):
            self.requests.append(request)
            return super().execute(request)

    transport = _Recording([{"id": "page-1", "title": "Notes"}])
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = transport
    image = io.BytesIO(b"\x89PNG fake bytes")
    image.name = "chart.png"

    client.me.onenote.sections["section-1"].pages.add(
        presentation_file=b"<html/>",
        attachment_files={"imageBlock1": image, "fileBlock1": b"raw-byte payload"},
    ).execute_query()

    body = transport.requests[-1].data
    assert b'name="imageBlock1"' in body and b"image/png" in body
    assert b'name="fileBlock1"' in body and b"application/octet-stream" in body


# --- a helper that dropped or mistyped what it was given ----------------------------


def test_a_verification_report_copies_its_lists():
    # ``to_dict`` aliased the lists it was given, so a later append changed a report
    # that had already been handed out.
    report = VerificationReport(
        source_count=2,
        target_count=2,
        checked=1,
        missing=["a.txt"],
        extra=["c.txt"],
        mismatches=["content mismatch: b.txt"],
        unverifiable=["versions: not supported"],
    )
    data = report.to_dict()

    report.missing.append("z.txt")
    assert data["missing"] == ["a.txt"]
    assert data["mismatches"] == ["content mismatch: b.txt"]
    assert data["unverifiable"] == ["versions: not supported"]
    assert data["ok"] is False
    assert data["complete"] is False


def test_a_client_result_answers_bytes_from_str_content():
    # A wrapper whose ``content`` is ``str`` was not converted, so a download wrote text.
    class _Wrapper:
        content = "text"

    assert ClientResult(None, _Wrapper()).to_bytes() == b"text"


def test_the_canvas_parser_skips_malformed_and_non_object_blobs():
    # A blob that is not a JSON object used to raise instead of being skipped.
    canvas = (
        '<div data-sp-controldata="{&quot;controlType&quot;:4}"></div>'
        '<div data-sp-controldata="{not json}"></div>'
        '<div data-sp-controldata="[1, 2]"></div>'
    )
    assert [control.control_type for control in parse_canvas_controls(canvas)] == [WEB_PART_CONTROL_TYPE]


def test_a_content_type_map_stores_only_the_identifiers_that_changed():
    class _ContentType:
        def __init__(self, name, string_id):
            self.name = name
            self.string_id = string_id

    source = [_ContentType("Item", "0x0100SOURCE"), _ContentType("Folder", "0x012000SAME")]
    target = [_ContentType("Item", "0x0100TARGET"), _ContentType("Folder", "0x012000SAME")]
    mapping = ContentTypeMap.build(source, target)

    assert mapping.entries == {"0x0100SOURCE": "0x0100TARGET"}
    assert mapping.resolve("0x01") == "0x01"
    assert mapping.resolve(None) is None


def test_a_package_encrypts_and_decrypts_with_its_key():
    # The key arrived base64-encoded from settings and was used as the raw string.
    raw = bytes(range(32))
    key = normalize_key(base64.b64encode(raw).decode("ascii"))

    ciphertext, iv = encrypt(b"hello world", key)

    assert ciphertext != b"hello world"
    assert len(base64.b64decode(iv)) == 16  # noqa: PLR2004
    assert decrypt(ciphertext, key, iv) == b"hello world"


def test_an_unset_credential_never_expires():
    for cred in (KeyCredential(), PasswordCredential()):
        assert cred.is_expired is False
        assert cred.days_until_expiry is None


def test_an_expired_credential_says_how_long_ago():
    status = KeyCredential(
        endDateTime=datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=3)
    ).expiry_status()
    assert status.status is CredentialExpiryStatus.EXPIRED
    assert str(status).startswith("expired ") and str(status).endswith("d ago")


def test_a_caml_query_knows_whether_it_is_paged():
    def query(xml: str) -> CamlQuery:
        parsed = CamlQuery()
        parsed.ViewXml = xml
        return parsed

    assert query("<View><RowLimit Paged='TRUE'>100</RowLimit></View>").is_paged
    assert query('<View><RowLimit Paged="TRUE">100</RowLimit></View>').is_paged
    assert not query("<View><RowLimit>100</RowLimit></View>").is_paged


def test_an_unpaged_query_over_sorted_columns_names_them():
    query = CamlQuery()
    query.ViewXml = "<View><Query><OrderBy><FieldRef Name='date'/></OrderBy></Query></View>"

    (message,) = threshold_warnings(query)

    assert "'date'" in message and "ensure_indexed" in message
    empty = CamlQuery()
    empty.ViewXml = "<View><Query></Query></View>"
    assert threshold_warnings(empty) == []
    with pytest.warns(UserWarning, match="not paged"):
        warn_if_unpaged(query)


# --- request shaping ----------------------------------------------------------------


def test_the_prefer_header_merges_what_each_helper_asks_for():
    request = RequestOptions(
        url="https://graph.microsoft.com/v1.0/groups", headers={"Prefer": "include-unknown-enum-members"}
    )
    prefer_upsert(request)
    prefer_upsert(request)
    assert request.headers["Prefer"] == (f"include-unknown-enum-members, {CREATE_IF_MISSING}, {RETURN_REPRESENTATION}")

    fresh = RequestOptions(url="https://graph.microsoft.com/v1.0/groups", headers={})
    prefer_create_if_missing(fresh)
    prefer_return_representation(fresh)
    prefer_outlook_timezone(fresh, "W. Europe Standard Time")
    assert fresh.headers["Prefer"] == (
        f'{CREATE_IF_MISSING}, {RETURN_REPRESENTATION}, outlook.timezone="W. Europe Standard Time"'
    )


def test_a_team_created_for_an_application_names_its_owners():
    # Application-context team creation requires an owner, and Graph accepts one only as
    # a conversation member: the payload *is* the contract. Nothing credentialed exercises
    # the ``owners`` argument, so this is where the rendering stays pinned.
    transport = RecordingTransport(
        [
            {
                "http_status": 202,
                "headers": {"Location": "https://graph.microsoft.com/v1.0/teams/abc/operations/op1"},
                "body": {},
            }
        ]
    )
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = transport

    client.teams.create("Team A", "desc", "standard", owners=["ada@contoso.com"]).execute_query()

    assert transport.requests[-1].data["members"] == [
        {
            "@odata.type": "#microsoft.graph.aadUserConversationMember",
            "roles": ["owner"],
            "user@odata.bind": "https://graph.microsoft.com/v1.0/users('ada@contoso.com')",
        }
    ]


def test_a_permanent_failure_is_not_retried():
    ctx = _context([{"status": 400}])
    ctx.with_auto_retry(max_retry=3, timeout_secs=1, jitter=False)

    with pytest.raises(ClientRequestException):
        ctx.load(ctx.web).execute_query()

    assert ctx.pending_request().transport.calls == 1


def test_a_denied_request_names_the_permission_it_needs():
    # A 401/403 raised a bare ``ClientRequestException``; the permission was in the
    # decorator on the builder method, unused.
    class _Response:
        status_code = 403
        reason = "Forbidden"
        url = "https://graph.microsoft.com/v1.0/security/cases/ediscoveryCases"
        _content = (
            b'{"error":{"code":"-2147024891, System.UnauthorizedAccessException",'
            b'"message":"Access denied. You do not have permission to perform this action."}}'
        )

    assert isinstance(ClientRequestException.from_response(_Response()), AccessDeniedException)

    client = _graph([{"status": 404, "body": {"error": {"code": "itemNotFound", "message": "gone"}}}])
    with pytest.raises(ObjectNotFoundException) as raised:
        client.drives.get().execute_query()
    assert raised.value.hints == ()


def test_an_async_denial_names_the_permission_too():
    from tests._scripted_transport import AsyncScriptedTransport

    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request()._async_transport = AsyncScriptedTransport(
        [{"status": 403, "body": {"error": {"code": "accessDenied", "message": "denied"}}}]
    )

    async def _run() -> str:
        with pytest.raises(AccessDeniedException) as raised:
            await client.drives.get().execute_query_async()
        return raised.value.hints[0]

    assert "Files.Read.All" in asyncio.run(_run())


def test_a_configured_credential_wins_over_session_auth(monkeypatch):
    # The session's basic auth replaced the NTLM provider the context was built with.
    monkeypatch.setattr(
        "office365.runtime.auth.providers.ntlm_provider.NtlmProvider.__init__",
        lambda self, credentials, *args, **kwargs: None,
    )
    monkeypatch.setattr(
        "office365.runtime.auth.providers.ntlm_provider.NtlmProvider.authenticate_request",
        lambda self, request: request.set_header("X-From-Provider", "1"),
    )
    session = requests.Session()
    session.auth = requests.auth.HTTPBasicAuth("DOMAIN\\user", "pwd")
    ctx = ClientContext("https://sp2019.contoso.local", allow_ntlm=True).with_transport(session=session)
    ctx.with_user_credentials("DOMAIN\\user", "pwd")

    request = RequestOptions("https://sp2019.contoso.local/_api/web")
    ctx.pending_request()._authenticate_request(request)

    assert request.headers["X-From-Provider"] == "1"


def test_has_application_permissions_answers_from_the_app_roles():
    graph_sp = {"id": "graph-sp", "displayName": "Microsoft Graph"}
    client = _graph(
        [
            {"value": [graph_sp]},
            {
                "id": "graph-sp",
                "appRoles": [{"id": "role-1", "value": "User.Read.All", "displayName": "Read users"}],
                "appRoleAssignedTo": [
                    {"id": "a", "appRoleId": "role-1", "principalId": "client-sp", "resourceId": "graph-sp"}
                ],
            },
            {"id": "client-sp"},
        ]
    )

    assert client.has_application_permissions("User.Read.All", "app-guid") is True


# --- conversions ----------------------------------------------------------------------


def test_a_profile_property_is_read_by_its_name():
    # A CSOM property bag keyed by ordinal read as ``{"0": {...}}``, so no name was
    # reachable at all.
    bag = {
        "0": {"Key": "0|UserProfile_GUID", "Value": "8b44de87-f8bf-4987-99f0", "ValueType": "Edm.Guid"},
        "1": {"Key": "0|AboutMe", "Value": "", "ValueType": "Edm.String"},
        "2": {"Key": "0|Skills", "Value": "Python", "ValueType": "Edm.String"},
        "3": {"Key": "0|IsAdmin", "Value": "true", "ValueType": "Edm.Boolean"},
    }
    ctx = _context([{"d": bag}])

    result = ctx.people_manager.get_user_profile_properties("i:0#.f|membership|mdoe@contoso.com").execute_query()

    # The ordinal prefix is the endpoint's, not the property's; ``ValueType`` types it.
    assert result.value == {
        "UserProfile_GUID": "8b44de87-f8bf-4987-99f0",
        "AboutMe": "",
        "Skills": "Python",
        "IsAdmin": True,
    }
    assert parse_key_value({"Key": "0|Skills", "Value": "Python", "ValueType": "Edm.String"}) == ("Skills", "Python")


def test_flags_that_no_single_member_spells_are_kept_as_sent():
    # ``parse_enum`` answered ``None`` for ``"password,voice"``, and a ``None`` column is
    # written back as null, so a read-and-sent-back policy lost it.
    assert parse_enum(AuthenticationMethodModes, "password,voice") == "password,voice"
    assert parse_enum(AuthenticationMethodModes, "password, voice") == "password, voice"
    assert parse_enum(AuthenticationMethodModes, "password") is AuthenticationMethodModes.password
    assert parse_enum(AuthenticationMethodModes, "1") is AuthenticationMethodModes.password
    assert parse_enum(AuthenticationMethodModes, "password,nonsense") is None
    assert parse_enum(ApplicationDataType, "documents") is ApplicationDataType.documents
    # The stored value reaches a payload as the service spelled it.
    stored = coerce_value(AuthenticationMethodModes, "password,voice", AuthenticationMethodModes.password, False)
    assert stored == "password,voice"


def test_planner_assignments_and_checklists_keep_their_wire_shape():
    # Open Types keyed by id: ``null`` removes an entry, and the server-managed
    # ``lastModifiedBy`` must not travel back.
    task = PlannerTask(GraphClient())
    task.set_property("assignments", {"u-9": {"orderHint": " !", "assignedDateTime": "2024-01-01T00:00:00Z"}}, False)
    ((user_id, assignment),) = list(task.assignments)
    assert user_id == "u-9"
    assert assignment.orderHint == " !"
    assert assignment.assignedDateTime is not None

    details = PlannerTaskDetails(GraphClient(), None)
    item_id = details.add_checklist_item("Draft", is_checked=True).checklist.add("Review")
    body = details.to_json(V4JsonFormat())["checklist"]
    assert body[item_id]["title"] == "Review"
    assert body[item_id]["isChecked"] is False
    assert "lastModifiedBy" not in body[item_id]

    details.checklist.remove(item_id)
    assert details.to_json(V4JsonFormat())["checklist"][item_id] is None
