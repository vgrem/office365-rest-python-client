"""What a tenant is licensed for, and what each licence carries.

Two questions look like one because both are answered by a licence list. What the *signed-in
user* holds is ``me/licenseDetails``: the SKUs assigned to that identity. What the *tenant*
bought is ``subscribedSkus``: a plan can be bought and assigned to nobody, and a tenant can
hold a SKU no user has. :meth:`Licences.of_user` and :meth:`Licences.of_tenant` are that
distinction, and a caller asking a licensing question says which one it means.

A SKU part number is packaging, not capability. ``DEVELOPERPACK_E5`` is a developer seat that
carries ``RECORDS_MANAGEMENT`` and ``PURVIEW_DISCOVERY``; a check written against the retail
SKUs alone (``SPE_E5``, ``M365_E5``, ...) answers "not licensed" for a user who can make the
call, because the decision was built out of a label. :attr:`Licences.names` returns both
spellings - the SKU when the question is packaging, the plan when the fact is a capability -
and only the plans the tenant has provisioned, because a plan that is not provisioned is not
held yet.

    >>> from office365.directory.licenses.tenant import Licences
    >>> held = Licences.of_user(client)
    >>> held.holds("M365_E5", "SPE_E5")  # either seat is enough
    True
    >>> [sku.sku_part_number for sku in held.carrying("RECORDS_MANAGEMENT")]
    ['M365_E5']

:meth:`Licences.of_tenant` answers the other question - which product carries a plan, and
what is bought but unassigned - which is the tenant-scoped form of the public licence matrix.
Only SKUs the tenant owns are visible here; the full product catalogue is Microsoft's
published data, not something Graph returns.

Nothing is copied out of the models: the items are the ``LicenseDetails`` and ``SubscribedSku``
the service returned, and this only answers the questions a requirement asks of them. Nothing
is cached either, because a licence changes while a program runs and a memoised answer is the
wrong one right after the grant that made it true. A caller that asks repeatedly should cache
at the level that knows when to forget - the test harness does, keyed on the run.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Iterator, Tuple

from office365.permissions import require_permission

if TYPE_CHECKING:
    from office365.directory.licenses.details import LicenseDetails
    from office365.directory.licenses.subscribed_sku import SubscribedSku
    from office365.graph_client import GraphClient


class Licences:
    """The licences an identity or a tenant holds, read once.

    Names are the service's spelling: SKU part numbers and plan names are reported in upper
    case (``ENTERPRISEPACK``, ``EXCHANGE_S_ENTERPRISE``), and comparison is exact so a typo
    cannot pass as a licence.
    """

    def __init__(self, items: Iterable[LicenseDetails | SubscribedSku] = ()) -> None:
        #: A licence with no part number names nothing a requirement could ask about.
        self._items: Tuple[LicenseDetails | SubscribedSku, ...] = tuple(i for i in items if i.sku_part_number)

    @classmethod
    @require_permission(delegated=["User.Read.All"], application=["User.Read.All"])
    def of_user(cls, client: GraphClient) -> Licences:
        """The SKUs assigned to the signed-in identity (``me/licenseDetails``)."""
        return cls(client.me.license_details.get().execute_query())

    @classmethod
    @require_permission(delegated=["Organization.Read.All"], application=["Organization.Read.All"])
    def of_tenant(cls, client: GraphClient) -> Licences:
        """The SKUs the tenant bought (``subscribedSkus``), assigned to users or not."""
        return cls(client.subscribed_skus.get().execute_query())

    @property
    def skus(self) -> Tuple[LicenseDetails | SubscribedSku, ...]:
        """The licences themselves, in the order the service listed them."""
        return self._items

    @property
    def names(self) -> frozenset[str]:
        """Every name a licence requirement may ask about: SKU part numbers and provisioned plans."""
        names: set[str] = set()
        for sku in self._items:
            names.add(sku.sku_part_number or "")
            names.update(_provisioned_plans(sku))
        return frozenset(names)

    def holds(self, *names: str) -> bool:
        """Whether any of ``names`` is held - the one-of semantics a requirement declares."""
        held = self.names
        return any(name in held for name in names)

    def carrying(self, plan: str) -> Tuple[LicenseDetails | SubscribedSku, ...]:
        """The licences whose provisioned plans include ``plan``."""
        return tuple(sku for sku in self._items if plan in _provisioned_plans(sku))

    def __iter__(self) -> Iterator[LicenseDetails | SubscribedSku]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)


def _provisioned_plans(sku: LicenseDetails | SubscribedSku) -> Tuple[str, ...]:
    """The plan names this licence turns on.

    Graph reports the state a plan reached (``Success``, ``PendingProvisioning``, ``Suspended``,
    ...); only one that reached ``Success`` is a plan a call can rely on.
    """
    return tuple(plan.servicePlanName or "" for plan in sku.service_plans or () if plan.provisioningStatus == "Success")
