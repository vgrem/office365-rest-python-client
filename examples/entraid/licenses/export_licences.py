"""Export every user's licence assignments as CSV — the input ``import_licences.py`` reads.

One row per user and SKU, with the plans disabled inside that SKU written by name. A SKU id is
only meaningful next to the tenant that issued it, and a plan id less so; the names are what
``import_licences.py`` accepts back. The columns and the naming are
``office365.directory.licenses.plan.assignments``; this script only picks the output.

    python export_licences.py > licences.csv

Requires ``User.Read.All`` and ``Organization.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-list-licensedetails
"""

import argparse
import sys

from office365.directory.licenses.plan import assignments
from office365.graph_client import GraphClient
from office365.runtime.converters.csv_writer import write_records
from tests.settings import client_id, client_secret, tenant


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    write_records(assignments(client), sys.stdout)


if __name__ == "__main__":
    main()
