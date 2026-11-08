"""What a licence change needs, decided before anything is sent.

:class:`~office365.directory.licenses.tenant.Licences` answers what is held; this answers what
*changes*. ``assignLicense`` takes the whole assignment for a SKU rather than an edit, so a SKU
already held with other disabled plans is re-added with the new set, and a SKU nobody asks for
any more is removed.

The preconditions Graph itself checks are decided here too — a user with no ``usageLocation``, a
SKU this tenant does not subscribe to, a SKU with no seat left — so a batch run can name the row
it will not send instead of catching the refusal afterwards.

The tabular form of an assignment lives here as well, one definition for both directions:
:func:`assignments` writes what the tenant holds, :func:`read_assignments` reads it back, and
both use the same three columns. A CSV is the contract of a fan-out that spans two types — a
user and the SKUs inside it — so neither the shape nor the naming is left to a script.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from os import PathLike
from typing import TYPE_CHECKING, Iterable, Iterator, Mapping, Tuple, Union

from office365.directory.licenses.assigned_license import AssignedLicense
from office365.runtime.types.collections import StringCollection

if TYPE_CHECKING:
    from office365.directory.licenses.subscribed_sku import SubscribedSku
    from office365.directory.users.user import User
    from office365.graph_client import GraphClient


@dataclass(frozen=True)
class LicenceChange:
    """One user's distance from what was asked, or the reason it will not be sent.

    ``add`` and ``remove`` are exactly the two arguments of ``assignLicense``. An empty pair
    means the user already holds what was asked — nothing to send. ``blocked_by`` names a
    precondition Graph would refuse on, so the caller reports it instead of discovering it.
    """

    user: User
    add: tuple[AssignedLicense, ...] = ()
    remove: tuple[str, ...] = ()
    blocked_by: str = ""

    @property
    def needed(self) -> bool:
        """Is there call to make once nothing blocks it?"""
        return bool(self.add or self.remove)

    def apply(self) -> User:
        """Queue the ``assignLicense`` call this change describes.

        Raises:
            ValueError: The change is blocked — the reason is ``blocked_by``.
        """
        if self.blocked_by:
            raise ValueError(f"{self.user.user_principal_name}: {self.blocked_by}")
        return self.user.assign_license(add_licenses=list(self.add), remove_licenses=list(self.remove))


def plan_licences(
    wanted: Mapping[User, Iterable[AssignedLicense]],
    *,
    skus: Iterable[SubscribedSku] = (),
) -> tuple[LicenceChange, ...]:
    """Decide what each user needs to hold the licences asked for.

    Every user in ``wanted`` gets a change, in the order given, so a report can count the rows
    that need nothing as well as the rows that need a call. Users must already be read, with
    ``assignedLicenses`` asked for: ``assignedLicenses`` is derived and absent from the default
    projection, so an unread or under-selected user looks like one holding nothing and would
    "assign" everything.

    Args:
        wanted (Mapping[User, Iterable[AssignedLicense]]): The licences each user should hold, as
            ``AssignedLicense`` values — a SKU id and the plans to disable inside it.
        skus (Iterable[SubscribedSku]): The tenant's catalogue, to decide seats and to name a SKU
            the tenant does not subscribe to. Omit it and those two checks are not made.

    Raises:
        ValueError: A user was never read (``is_loaded`` is ``False``) or was read without
            ``assignedLicenses`` in the projection.
    """
    catalogue = _catalogue(skus)
    return tuple(_change_for(user, licences, catalogue) for user, licences in wanted.items())


def _change_for(
    user: User,
    licences: Iterable[AssignedLicense],
    catalogue: Mapping[str, tuple[str, int]],
) -> LicenceChange:
    if not user.is_loaded:
        raise ValueError(f"{user.resource_path}: read the user before planning its licences")
    if not user.is_property_available("assignedLicenses"):
        raise ValueError(
            f"{user.resource_path}: ask for assignedLicenses when reading the user "
            "— a projection without it holds nothing and would assign everything"
        )

    asked = {str(licence.skuId): frozenset(str(plan) for plan in licence.disabledPlans) for licence in licences}
    held = {
        str(licence.skuId): frozenset(str(plan) for plan in licence.disabledPlans) for licence in user.assigned_licenses
    }
    add = tuple(
        AssignedLicense(skuId=sku_id, disabledPlans=StringCollection(sorted(plans)))
        for sku_id, plans in asked.items()
        if held.get(sku_id) != plans
    )
    remove = tuple(sku_id for sku_id in held if sku_id not in asked)
    return LicenceChange(user, add, remove, _blocked_by(user, add, remove, catalogue))


def _blocked_by(
    user: User,
    add: tuple[AssignedLicense, ...],
    remove: tuple[str, ...],
    catalogue: Mapping[str, tuple[str, int]],
) -> str:
    if add:
        if not user.usage_location:
            return "no usageLocation, so no licence can be assigned"
        for licence in add:
            if not catalogue:
                break
            part_number, seats_left = catalogue.get(str(licence.skuId), ("", 0))
            if not part_number:
                return f"{licence.skuId} is not a SKU this tenant subscribes to"
            if seats_left <= 0:
                return f"{part_number} has no seat left"
    inherited = _inherited(user)
    for sku_id in remove:
        if sku_id in inherited:
            return f"{_named(sku_id, catalogue)} is held through group {inherited[sku_id]}; change the group"
    return ""


def _inherited(user: User) -> dict[str, str]:
    """The SKU ids a group grants, and the group that grants them.

    A licence inherited from a group is in ``assignedLicenses`` like any other, but
    ``assignLicense`` cannot remove it — the group owns it. Naming the group is the answer
    to "why will this not go away".
    """
    return {
        str(state.skuId): str(state.assignedByGroup) for state in user.license_assignment_states if state.assignedByGroup
    }


def _named(sku_id: str, catalogue: Mapping[str, tuple[str, int]]) -> str:
    return catalogue.get(sku_id, (sku_id, 0))[0]


# ── The tabular form ─────────────────────────────────────────────


def assignments(client: GraphClient) -> Iterator[dict[str, str]]:
    """Every user's licences as one record per user and SKU.

    ``assignedLicenses`` is derived and absent from a user's default projection, so the holders
    are read with it selected — and asked for by number, not by page
    (``$filter=assignedLicenses/$count ne 0``). A SKU id means nothing outside the tenant that
    issued it and a plan id less, so a record carries the part number and the plan names, as
    ``user_principal_name``, ``sku``, ``disabled_plans``. A SKU the tenant no longer subscribes
    to is still reported, by id, rather than dropped: a row that vanished would read as a
    licence nobody has. The walk loads every holder before yielding, so a tenant too large for
    that wants the paged exporter instead of this generator.

    >>> from office365.runtime.converters.csv_writer import write_records
    >>> write_records(assignments(client), sys.stdout)
    """
    catalogue = {str(sku.sku_id): sku for sku in client.subscribed_skus.get().execute_query()}
    holders = client.users.select(["userPrincipalName", "assignedLicenses"]).get_licensed()
    holders.get_all().execute_query()
    for user in holders:
        for licence in user.assigned_licenses:
            sku = catalogue.get(str(licence.skuId))
            yield {
                "user_principal_name": user.user_principal_name or "",
                "sku": (sku.sku_part_number if sku else None) or str(licence.skuId),
                "disabled_plans": ",".join(sorted(licence.disabled_plan_names(sku))),
            }


def read_assignments(source: Union[str, PathLike[str]]) -> dict[str, list[Tuple[str, list[str]]]]:
    """Read an assignment list: user principal name -> ``(SKU part number, disabled plans)``.

    The shape :func:`assignments` writes, in file order, with the plans still named. Resolving
    a name to an id is the tenant's job (``SubscribedSku.plan_id``), so a list written by one
    tenant reads against another without an id table in between.
    """
    wanted: dict[str, list[Tuple[str, list[str]]]] = {}
    with open(source, encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            plans = [name for name in (row.get("disabled_plans") or "").split(",") if name]
            wanted.setdefault(row["user_principal_name"], []).append((row["sku"], plans))
    return wanted


def _catalogue(skus: Iterable[SubscribedSku]) -> dict[str, tuple[str, int]]:
    """Seats left per SKU id, with the part number to name it by."""
    return {
        str(sku.sku_id): (sku.sku_part_number or "", (sku.prepaid_units.enabled or 0) - (sku.consumed_units or 0))
        for sku in skus
    }
