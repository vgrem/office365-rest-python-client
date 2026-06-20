"""
Find application registrations and service principals without owners.

Required delegated permissions: Application.Read.All,
ServicePrincipal.Read.All, User.Read.All.
"""

from office365.graph_client import GraphClient
from office365.runtime.http.request_options import RequestOptions
from tests import test_client_id, test_client_secret, test_tenant


def _set_consistency(request: RequestOptions) -> None:
    request.ensure_header("ConsistencyLevel", "eventual")


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    client.pending_request().beforeExecute += _set_consistency

    apps_qry = client.applications.filter("owners/$count eq 0").select(["displayName", "createdDateTime"])
    apps_qry.query_options.custom["count"] = "true"
    apps = apps_qry.get().execute_query()

    sps_qry = client.service_principals.filter("owners/$count eq 0").select(["displayName"])
    sps_qry.query_options.custom["count"] = "true"
    sps = sps_qry.get().execute_query()

    client.pending_request().beforeExecute -= _set_consistency

    total = len(apps) + len(sps)
    if apps:
        for a in sorted(apps, key=lambda x: x.display_name or ""):
            print(f"  {a.display_name}  ({a.created_date_time.date()})")
    if sps:
        print()
        for s in sorted(sps, key=lambda x: x.display_name or ""):
            print(f"  {s.display_name}")
    print(f"\nTotal orphaned: {total}")


if __name__ == "__main__":
    main()
