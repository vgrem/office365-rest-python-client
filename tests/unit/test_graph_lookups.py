"""Offline tests for the Phase 2 Graph lookup helpers.

Every lookup is *deferred* (nothing hits the wire until ``execute_query()``) and
*tolerant*: a miss leaves the returned entity uninitialized instead of raising,
detected via ``is_loaded``.
"""

from __future__ import annotations

from urllib.parse import unquote_plus

from office365.booking.business.business import BookingBusiness
from office365.directory.licenses.subscribed_sku import SubscribedSku
from office365.directory.users.user import User
from office365.graph_client import GraphClient
from office365.intune.devices.management.managed.managed import ManagedDevice
from office365.teams.team import Team
from tests._scripted_transport import ScriptedTransport

USER = {"id": "u1", "displayName": "Ada Lovelace", "mail": "ada@contoso.com"}
TEAM = {"id": "g1", "displayName": "Team One", "resourceProvisioningOptions": ["Team"]}
BUSINESS = {"id": "b1", "displayName": "Contoso Bookings"}
DEVICE = {"id": "d1", "deviceName": "DESKTOP-1"}
SKU = {"id": "s1", "skuId": "sku-guid", "skuPartNumber": "ENTERPRISEPACK"}


class _RecordingTransport(ScriptedTransport):
    """Scripted transport that also records the request URLs it received."""

    def __init__(self, payloads):
        super().__init__(payloads)
        self.urls: list[str] = []

    def execute(self, request):
        self.urls.append(request.url)
        return super().execute(request)


def _client(payloads):
    transport = _RecordingTransport(payloads)
    client = GraphClient()
    client.pending_request().beforeExecute.clear()
    client.pending_request().transport = transport
    return client, transport


def test_get_by_mail_defers_and_returns_match():
    client, transport = _client([{"value": [USER]}])

    user = client.users.get_by_mail("ada@contoso.com")

    assert transport.urls == []
    assert not user.is_loaded

    user.execute_query()

    assert isinstance(user, User)
    assert user.is_loaded
    assert user.get_property("id") == "u1"
    assert len(transport.urls) == 1
    assert "/users" in transport.urls[0]
    assert "mail eq 'ada@contoso.com'" in unquote_plus(transport.urls[0])


def test_get_by_mail_uninitialized_when_absent():
    client, _ = _client([{"value": []}])

    user = client.users.get_by_mail("nobody@contoso.com").execute_query()

    assert not user.is_loaded
    assert user.get_property("id") is None


def test_team_get_by_name_defers_and_returns_team():
    client, transport = _client([{"value": [TEAM]}])

    team = client.teams.get_by_name("Team One")

    assert transport.urls == []
    assert not team.is_loaded

    team.execute_query()

    assert isinstance(team, Team)
    assert team.is_loaded
    assert team.get_property("id") == "g1"
    url = unquote_plus(transport.urls[0])
    assert "/groups" in url
    assert "resourceProvisioningOptions/Any(x:x eq 'Team')" in url
    assert "displayName eq 'Team One'" in url


def test_team_get_by_name_miss_is_uninitialized():
    client, _ = _client([{"value": []}])

    team = client.teams.get_by_name("Missing Team").execute_query()

    assert not team.is_loaded
    assert team.get_property("id") is None


def test_team_get_by_name_sets_entity_path_from_group_id():
    client, _ = _client([{"value": [TEAM]}])

    team = client.teams.get_by_name("Team One").execute_query()

    assert team.resource_url.endswith("/teams/g1")


def test_booking_get_by_name_matches_client_side():
    client, transport = _client([{"value": [{"id": "b0", "displayName": "Other"}, BUSINESS]}])

    business = client.solutions.booking_businesses.get_by_name("Contoso Bookings")

    assert transport.urls == []
    assert not business.is_loaded

    business.execute_query()

    assert isinstance(business, BookingBusiness)
    assert business.is_loaded
    assert business.get_property("id") == "b1"
    assert "/solutions/bookingBusinesses" in transport.urls[0]
    assert "$filter" not in transport.urls[0]


def test_booking_get_by_name_uninitialized_when_absent():
    client, _ = _client([{"value": [{"id": "b0", "displayName": "Other"}]}])

    business = client.solutions.booking_businesses.get_by_name("Missing").execute_query()

    assert not business.is_loaded


def test_managed_device_get_by_name_defers_and_returns_device():
    client, transport = _client([{"value": [DEVICE]}])

    device = client.device_management.managed_devices.get_by_name("DESKTOP-1")

    assert transport.urls == []
    assert not device.is_loaded

    device.execute_query()

    assert isinstance(device, ManagedDevice)
    assert device.is_loaded
    assert device.get_property("id") == "d1"
    url = unquote_plus(transport.urls[0])
    assert "/deviceManagement/managedDevices" in url
    assert "deviceName eq 'DESKTOP-1'" in url


def test_managed_device_get_by_name_uninitialized_when_absent():
    client, _ = _client([{"value": []}])

    device = client.device_management.managed_devices.get_by_name("NOPE").execute_query()

    assert not device.is_loaded


def test_subscribed_sku_get_by_part_number_is_case_insensitive():
    client, transport = _client([{"value": [SKU]}])

    sku = client.subscribed_skus.get_by_part_number("enterprisepack")

    assert transport.urls == []
    assert not sku.is_loaded

    sku.execute_query()

    assert isinstance(sku, SubscribedSku)
    assert sku.is_loaded
    assert sku.get_property("id") == "s1"
    assert "/subscribedSkus" in transport.urls[0]


def test_subscribed_sku_get_by_part_number_uninitialized_when_absent():
    client, _ = _client([{"value": [SKU]}])

    sku = client.subscribed_skus.get_by_part_number("NOT_A_SKU").execute_query()

    assert not sku.is_loaded
