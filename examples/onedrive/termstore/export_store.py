"""
Import a taxonomy hierarchy into a Microsoft Graph term store from JSON or CSV.

JSON format mirrors the term store model:
  [group { name, sets: [ set { name, children: [ term { name, children: [] } ] } ] }]

CSV format:
  group,set,term,parent_term
  Rows are processed in order — parents must appear before children.

Requires delegated permission TermStore.ReadWrite.All.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username


def main():
    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    store = client.sites.root.term_store
    result = store.export_to_json().execute_query()
    print(f"Exported into {result.value}")


if __name__ == "__main__":
    main()
