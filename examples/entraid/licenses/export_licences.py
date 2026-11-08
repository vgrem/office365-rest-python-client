"""Export every user's licence assignments as CSV — the input ``import_licences.py`` reads.

A row is a user and a SKU, and the columns after the user are the licence's own: ``skuId``
and the ``disabledPlans`` inside it. Graph will not project them — ``$expand`` answers
"not a navigation property or complex property" and ``$select=assignedLicenses/skuId``
answers "Invalid property 'skuId' specified in $select" — so the row unit is stated to the
exporter with ``rows_from`` and the projection asks only for the column that says whose row
it is.

    python export_licences.py > licences.csv

Requires ``User.Read.All``.

https://learn.microsoft.com/en-us/graph/api/resources/assignedlicense
"""

import argparse
import sys

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    licensed = client.users.get_licensed().select(["userPrincipalName"]).get_all()
    licensed.to_csv(sys.stdout, rows_from="assignedLicenses").execute_query()


if __name__ == "__main__":
    main()
