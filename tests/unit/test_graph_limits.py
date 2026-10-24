"""Unit tests for model-bound Microsoft Graph throttling quotas."""

from __future__ import annotations

from office365.communications.callrecords.call_record import CallRecord
from office365.directory.domains.domain import Domain
from office365.directory.licenses.subscribed_sku import SubscribedSku
from office365.directory.objects.object import DirectoryObject
from office365.runtime.limits import Limit


def test_identity_quotas_declared_on_directory_object():
    limits = DirectoryObject.declared_limits()
    assert limits, "DirectoryObject should declare the identity quotas"
    assert all(isinstance(limit, Limit) for limit in limits)
    assert {limit.name for limit in limits} == {"identity"}
    assert any(limit.unit == "resource_units" and limit.is_rate for limit in limits)


def test_identity_on_subscribed_sku_and_domain():
    assert any(limit.name == "identity" for limit in SubscribedSku.declared_limits())
    assert any(limit.name == "identity" for limit in Domain.declared_limits())


def test_call_record_limits_name_every_scope_that_applies():
    # The type answers with its own budgets *and* the ceiling its navigations carry:
    # three budgets on the resource family, one per-record ceiling on the children.
    limits = CallRecord.declared_limits()
    assert {limit.scope for limit in limits} == {"app", "tenant", "app+tenant", "call record"}
