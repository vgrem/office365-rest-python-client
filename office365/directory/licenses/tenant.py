"""What a tenant is licensed for, and what each licence carries.

Two questions look like one because both are answered by a licence list. What a *user* holds is
``/users/{id}/licenseDetails``: the SKUs assigned to that identity. What the *tenant* bought is
``subscribedSkus``: a plan can be bought and assigned to nobody, and a tenant can hold a SKU no
user has. :meth:`LicenceManager.get_user` and :meth:`LicenceManager.get_all` are that
distinction, and a caller asking a licensing question says which one it means.

A SKU part number is packaging, not capability. ``DEVELOPERPACK_E5`` is a developer seat that
carries ``RECORDS_MANAGEMENT`` and ``PURVIEW_DISCOVERY``; a check written against the retail
SKUs alone (``SPE_E5``, ``M365_E5``, ...) answers "not licensed" for a user who can make the
call, because the decision was built out of a label. :attr:`LicencesReport.names` returns both
spellings - the SKU when the question is packaging, the plan when the fact is a capability -
and only the plans the tenant has provisioned, because a plan that is not provisioned is not
held yet.

    >>> result = client.licences.get_all().execute_query()  # one read
    >>> held = result.value
    >>> held.holds("M365_E5", "SPE_E5")  # either seat is enough
    True
    >>> [sku.sku_part_number for sku in held.carrying("RECORDS_MANAGEMENT")]
    ['M365_E5']
    >>> [sku.sku_part_number for sku in held.unassigned]
    ['M365_E5']

``client.licences`` is the manager, and reaching it sends nothing;
``get_all()`` (or ``get_user(client.me)``) queues the read and hands back a
:class:`~office365.runtime.client_result.ClientResult`, exactly like every other deferred call in
the library. ``execute_query()`` sends it and ``.value`` is the :class:`LicencesReport`, which
then answers any number of questions without another round trip. A licence is granted while a
program runs, so the read happens where the decision is rather than being quietly kept.

What comes back is only what the tenant owns. The full product catalogue - which retail SKU
carries which plan, what is not bought yet - is Microsoft's published data, not something Graph
returns, so it is not this module's business to carry a copy of it.

Nothing is copied out of the models: the items are the ``LicenseDetails`` and ``SubscribedSku``
the service returned, and the report only answers the questions a requirement or a report asks
of them.
"""

from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

from office365.directory.licenses.subscribed_sku import SubscribedSku
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value import ClientValue

if TYPE_CHECKING:
    from office365.directory.licenses.details import LicenseDetails
    from office365.directory.users.user import User
    from office365.graph_client import GraphClient

#: The ``capabilityStatus`` values that mean the seats cannot be handed out.
_UNUSABLE = frozenset({"Suspended", "LockedOut", "Deleted"})


class LicenceManager:
    """The licensing questions a client can ask, each of them a deferred read.

    Reaching the manager sends nothing and keeps nothing: a licence changes while a program
    runs, so the read belongs where the decision is.
    """

    def __init__(self, client: GraphClient) -> None:
        self._client = client

    @require_permission(delegated=["Organization.Read.All"], application=["Organization.Read.All"])
    def get_all(self) -> ClientResult[LicencesReport]:
        """The SKUs the tenant bought (``subscribedSkus``), assigned to users or not.

        >>> held = client.licences.get_all().execute_query().value
        """
        return _deferred(self._client.subscribed_skus)

    @require_permission(delegated=["User.Read.All"], application=["User.Read.All"])
    def get_user(self, user: User | str) -> ClientResult[LicencesReport]:
        """The SKUs assigned to one user (``/users/{id}/licenseDetails``).

        ``user`` is a :class:`~office365.directory.users.user.User` - ``client.me`` is one - or the
        id / user principal name Graph addresses a user by, so the signed-in identity is
        ``get_user(client.me)``.

            >>> mine = client.licences.get_user(client.me).execute_query().value
            >>> hers = client.licences.get_user("ada@contoso.com").execute_query().value
        """
        target = self._client.users.get_by_principal_name(user) if isinstance(user, str) else user
        return _deferred(target.license_details)


class LicencesReport(ClientValue):
    """The licences an identity or a tenant holds, and what each of them turns on.

    Names are the service's spelling: SKU part numbers and plan names are reported in upper
    case (``ENTERPRISEPACK``, ``EXCHANGE_S_ENTERPRISE``), and comparison is exact so a typo
    cannot pass as a licence.
    """

    #: The licences themselves, in the order the service listed them. A licence with no part
    #: number names nothing a requirement could ask about, so it is not kept. Iterated as
    #: ``report.skus`` - a value's own ``__iter__`` is what serialises it.
    skus: List[Any] = field(default_factory=list)

    @property
    def names(self) -> frozenset[str]:
        """Every name a licence requirement may ask about: SKU part numbers and provisioned plans."""
        names: set[str] = set()
        for sku in self.skus:
            names.add(sku.sku_part_number or "")
            names.update(_provisioned_plans(sku))
        return frozenset(names)

    @property
    def plans(self) -> frozenset[str]:
        """The capability vocabulary alone: the provisioned plan names, without the packaging."""
        return frozenset(name for sku in self.skus for name in _provisioned_plans(sku))

    @property
    def unassigned(self) -> Tuple[SubscribedSku, ...]:
        """The SKUs with seats bought and not handed out - usually what a licence report is asked.

        Empty for :meth:`LicenceManager.get_user`, whose items are assignments and carry no
        seat counts.
        """
        return tuple(sku for sku in self._tenant_skus() if _has_spare_seat(sku))

    @property
    def by_id(self) -> Dict[str, SubscribedSku]:
        """The tenant SKUs keyed by ``skuId``, which is how an assignment names the SKU it holds."""
        return {sku.sku_id: sku for sku in self._tenant_skus() if sku.sku_id}

    def to_rows(self) -> List[Dict[str, Any]]:
        """One row per tenant SKU, with the columns spelled the way the service spells them.

        What a licence report is asked for - seats bought, seats handed out, seats left - in the
        shape ``csv.DictWriter`` and a dataframe both take.
        """
        return [
            {
                "skuId": sku.sku_id,
                "skuPartNumber": sku.sku_part_number,
                "capabilityStatus": sku.capability_status,
                "prepaidUnits": sku.prepaid_units.enabled or 0,
                "consumedUnits": sku.consumed_units or 0,
                "spareUnits": max((sku.prepaid_units.enabled or 0) - (sku.consumed_units or 0), 0),
                "servicePlans": len(_provisioned_plans(sku)),
            }
            for sku in self._tenant_skus()
        ]

    @property
    def suspended(self) -> Tuple[SubscribedSku, ...]:
        """The SKUs whose ``capabilityStatus`` says the seats cannot be assigned from."""
        return tuple(sku for sku in self._tenant_skus() if (sku.capability_status or "") in _UNUSABLE)

    def holds(self, *names: str) -> bool:
        """Whether any of ``names`` is held - the one-of semantics a requirement declares."""
        held = self.names
        return any(name in held for name in names)

    def carrying(self, plan: str) -> Tuple[LicenseDetails | SubscribedSku, ...]:
        """The licences whose provisioned plans include ``plan``."""
        return tuple(sku for sku in self.skus if plan in _provisioned_plans(sku))

    def plan_id(self, name: str) -> Optional[str]:
        """The id of the plan named ``name``, or ``None`` when no licence here carries it.

        The id is the join key: a part number is packaging and a plan name is a spelling, but an
        id is the same string on both sides of an assignment.
        """
        for sku in self._tenant_skus():
            plan_id = sku.plan_id(name)
            if plan_id is not None:
                return plan_id
        return None

    def plan_name(self, plan_id: str) -> Optional[str]:
        """The name of the plan with this id, or ``None`` when no licence here carries it."""
        for sku in self._tenant_skus():
            if any(plan.service_plan_id == plan_id for plan in sku.service_plans):
                return sku.plan_name(plan_id)
        return None

    def _tenant_skus(self) -> Tuple[SubscribedSku, ...]:
        """The items that carry seat counts and statuses (``subscribedSkus``), not assignments."""
        return tuple(sku for sku in self.skus if isinstance(sku, SubscribedSku))


def _deferred(source: Any) -> ClientResult[LicencesReport]:
    """Queue the read behind ``source`` and hand back the result that will hold the report.

    The read is queued, not sent: ``execute_query()`` on the returned result submits it, and what
    the service listed lands in ``result.value``.
    """
    result = ClientResult(source.context, LicencesReport())
    report = result.value

    def _listed(items: Any) -> None:
        report.skus = [item for item in items if item.sku_part_number]

    source.get().after_execute(_listed)
    return result


def _provisioned_plans(sku: LicenseDetails | SubscribedSku) -> Tuple[str, ...]:
    """The plan names this licence turns on.

    Graph reports the state a plan reached (``Success``, ``PendingProvisioning``, ``Suspended``,
    ...); only one that reached ``Success`` is a plan a call can rely on.
    """
    return tuple(
        plan.service_plan_name or "" for plan in sku.service_plans or () if plan.provisioning_status == "Success"
    )


def _has_spare_seat(sku: SubscribedSku) -> bool:
    """Whether the SKU has a seat bought that nobody is using."""
    return (sku.consumed_units or 0) < (sku.prepaid_units.enabled or 0)
