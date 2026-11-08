"""Give the users a CSV names the licences it asks for — and say what each row needs first.

The CSV is the shape ``export_licences.py`` writes: one row per user and SKU, with the plans
disabled inside that SKU written by name. Every row is planned before anything is sent, so
"already held", "blocked" and "needs a call" are different answers rather than a failed call.
``--dry-run`` stops at the plan.

    python import_licences.py licences.csv --dry-run
    python import_licences.py licences.csv

A licence inherited from a group is reported, not removed: the group owns it. For a population,
group-based licensing is the way round; this fan-out is for a one-off list.

Requires ``User.ReadWrite.All`` and ``Organization.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-assignlicense
"""

import argparse
import csv
from collections import defaultdict

from office365.directory.licenses.assigned_license import AssignedLicense
from office365.directory.licenses.plan import LicenceChange, plan_licences
from office365.directory.licenses.subscribed_sku import SubscribedSku
from office365.graph_client import GraphClient
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.types.collections import StringCollection
from tests.settings import client_id, client_secret, tenant


def asked_licences(rows: list[tuple[str, list[str]]], catalogue: dict[str, SubscribedSku]) -> list[AssignedLicense]:
    """The rows of one user as ``assignLicense`` wants them — names resolved against the SKU."""
    licences = []
    for part_number, names in rows:
        sku = catalogue.get(part_number)
        if sku is None:
            raise LookupError(f"this tenant subscribes to no SKU named {part_number}")
        plan_ids = {name: sku.plan_id(name) for name in names}
        unknown = [name for name, plan_id in plan_ids.items() if plan_id is None]
        if unknown:
            raise LookupError(f"{part_number} has no plan named {', '.join(unknown)}")
        disabled = StringCollection([plan_id for plan_id in plan_ids.values() if plan_id])
        licences.append(AssignedLicense(skuId=sku.sku_id, disabledPlans=disabled))
    return licences


def describe(change: LicenceChange, parts_by_id: dict[str, str]) -> str:
    """The SKUs going on and off, named the way the CSV names them."""
    added = [f"+{parts_by_id.get(str(licence.skuId), licence.skuId)}" for licence in change.add]
    return ", ".join(added + [f"-{parts_by_id.get(sku_id, sku_id)}" for sku_id in change.remove])


def read_rows(path: str) -> dict[str, list[tuple[str, list[str]]]]:
    wanted: dict[str, list[tuple[str, list[str]]]] = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            names = [name for name in (row.get("disabled_plans") or "").split(",") if name]
            wanted[row["user_principal_name"]].append((row["sku"], names))
    return wanted


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", help="CSV written by export_licences.py")
    parser.add_argument("--dry-run", action="store_true", help="Print what each row needs, send nothing")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    skus = client.subscribed_skus.get().execute_query()
    parts_by_id = {str(sku.sku_id): sku.sku_part_number or "" for sku in skus}

    for upn, rows in read_rows(args.path).items():
        try:
            asked = asked_licences(rows, {sku.sku_part_number or "": sku for sku in skus})
        except LookupError as error:
            print(f"{upn}: {error}")
            continue
        try:
            user = client.users.get_by_principal_name(upn)
            user.select(["id", "userPrincipalName", "usageLocation", "assignedLicenses", "licenseAssignmentStates"])
            user.get().execute_query()
        except ClientRequestException as error:
            print(f"{upn}: not read — {error}")
            continue

        change = plan_licences({user: asked}, skus=skus)[0]
        if change.blocked_by:
            print(f"{upn}: blocked — {change.blocked_by}")
        elif not change.needed:
            print(f"{upn}: already held")
        elif args.dry_run:
            print(f"{upn}: would set {describe(change, parts_by_id)}")
        else:
            change.apply().execute_query()
            print(f"{upn}: set {describe(change, parts_by_id)}")


if __name__ == "__main__":
    main()
