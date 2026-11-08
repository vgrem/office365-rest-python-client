"""Give the users a CSV names the licences it asks for — and say what each row needs first.

The CSV is the shape ``export_licences.py`` writes: one row per user and SKU, the columns after
the user being the licence's own. Every row is planned before anything is sent, so
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

from office365.directory.licenses.assigned_license import AssignedLicense
from office365.directory.licenses.plan import LicenceChange, plan_licences
from office365.graph_client import GraphClient
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.types.collections import StringCollection
from tests.settings import client_id, client_secret, tenant


def read_rows(path: str) -> dict[str, list[tuple[str, list[str]]]]:
    """User principal name -> what the file asks for them: ``[(SKU id, disabled plan ids)]``."""
    wanted: dict[str, list[tuple[str, list[str]]]] = {}
    with open(path, encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            disabled = [plan for plan in row["disabledPlans"].split("; ") if plan]
            wanted.setdefault(row["userPrincipalName"], []).append((row["skuId"], disabled))
    return wanted


def asked_licences(rows: list[tuple[str, list[str]]]) -> list[AssignedLicense]:
    """The rows of one user as ``assignLicense`` wants them — the ids the file carries."""
    return [AssignedLicense(skuId=sku_id, disabledPlans=StringCollection(disabled)) for sku_id, disabled in rows]


def describe(change: LicenceChange, parts_by_id: dict[str, str]) -> str:
    """The SKUs going on and off, named the way the CSV names them."""
    added = [f"+{parts_by_id.get(str(licence.skuId), licence.skuId)}" for licence in change.add]
    return ", ".join(added + [f"-{parts_by_id.get(sku_id, sku_id)}" for sku_id in change.remove])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", help="CSV written by export_licences.py")
    parser.add_argument("--dry-run", action="store_true", help="Print what each row needs, send nothing")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    skus = client.subscribed_skus.get().execute_query()
    parts_by_id = {str(sku.sku_id): sku.sku_part_number or "" for sku in skus}

    for upn, rows in read_rows(args.path).items():
        asked = asked_licences(rows)
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
