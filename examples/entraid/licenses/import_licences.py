"""Assign the licences a CSV asks for — one ``assignLicense`` per row, in as few batches as fit.

The CSV is the shape ``export_licences.py`` writes: one row per user and SKU, so the columns
after ``userPrincipalName`` are the licence's own. Reading it is one call, because the type
names the columns; then the row becomes the verb's own body:

    read    deserialize_records(AssignedLicense, path, format="csv")
    shape   {"userPrincipalName": …, "addLicenses": [licence]}
    send    client.users.assign_licences(rows)  +  client.execute_batch()

``allow_unknown=True`` is what lets a row carry ``userPrincipalName``: the licence does not
declare it, the file needs it to address the user. Nothing is read first — the
``/users/{user-id}`` segment takes a UPN or an id — and nothing is decided here: Graph owns the
preconditions (no ``usageLocation``, a SKU this tenant does not subscribe to, no seat left), so a
row it refuses comes back as that sub-request's error.

    python import_licences.py licences.csv --dry-run
    python import_licences.py licences.csv

Removing is the same verb with the other argument: a row reads
``{"id": …, "removeLicenses": [sku_id]}``. A licence inherited from a group cannot be removed —
the group owns it — so that row fails, and says why.

Requires ``User.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/user-assignlicense
"""

import argparse

from office365.directory.licenses.assigned_license import AssignedLicense
from office365.graph_client import GraphClient
from office365.runtime.converters.records import deserialize_records
from tests.settings import client_id, client_secret, tenant


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", help="CSV written by export_licences.py")
    parser.add_argument("--dry-run", action="store_true", help="Print the rows, send nothing")
    args = parser.parse_args()

    # One row of the file is one licence for one user: the unit assignLicense takes.
    assignments = []
    for record in deserialize_records(AssignedLicense, args.path, format="csv", allow_unknown=True):
        upn = record.pop("userPrincipalName")  # the one column the licence does not declare
        assignments.append({"userPrincipalName": upn, "addLicenses": [AssignedLicense().hydrate(record)]})

    if args.dry_run:
        for row in assignments:
            print(f"{row['userPrincipalName']}: +{row['addLicenses'][0].skuId}")
        return

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    client.users.assign_licences(assignments)
    client.execute_batch()  # 20 sub-requests per $batch, one failed row does not stop the rest


if __name__ == "__main__":
    main()
