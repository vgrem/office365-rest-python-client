"""
Server-side migration into a SharePoint document library (full fidelity).

Packages a local directory as a SharePoint Migration API package, stages it in
SharePoint-owned Azure containers, and ingests it **server-side** — the only path
that preserves version history and ACLs.

Steps:
  1. authenticate — the Migration API requires app-only auth
  2. resolve the destination web + library
  3. provision the migration containers (SharePoint-owned; no Azure account)
  4. migrate — plan -> run: builds the manifest XML, stages the blobs, submits
  5. monitor — poll GetMigrationJobProgress until the job is terminal

Requires: an app registration with **Sites.FullControl.All** (application) and
write access to the target library. Certificate auth is used below; a client
secret (`with_client_secret`) is equally app-only.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/migration-api-overview
"""

from __future__ import annotations

import argparse
from urllib.parse import urlparse

from office365.migration import MigrationJob
from office365.migration.adapters.filesystem import FileSystemSource
from office365.migration.sharepoint.package_target import SharePointPackageTarget
from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def on_progress(progress) -> None:
    total = progress.total or "?"
    percent = f"{progress.percent:.0f}%" if progress.percent is not None else ""
    print(f"  {progress.stage}: {progress.done}/{total} {percent}".rstrip(), flush=True)


def main():
    parser = argparse.ArgumentParser(description="Server-side migration into a document library")
    parser.add_argument("--source", required=True, help="local directory to migrate")
    parser.add_argument("--library-url", default="Shared Documents", help="server-relative library URL")
    parser.add_argument("--interval", type=float, default=30, help="seconds between progress polls")
    args = parser.parse_args()

    # 1. Authenticate — the Migration API needs app-only (certificate) auth.
    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    # 2. Resolve the destination web + library.
    web = ctx.web.get().execute_query()
    web_url = urlparse(site_url).path or "/"
    library_url = "/" + args.library_url.strip("/")
    library_title = library_url.rsplit("/", 1)[-1]
    ctx.web.get_folder_by_server_relative_url(library_url).get().execute_query()  # fail fast if missing
    print(f"Target: {web_url} / {library_title} (web {web.id})")

    # 3. Provision SharePoint-owned Azure containers (SAS URIs + encryption key).
    containers = ctx.site.provision_migration_containers().execute_query().value
    print("Provisioned migration containers (no Azure account needed)")

    # 4. Migrate — build the manifest XML, stage the blobs, submit the ingestion job.
    target = SharePointPackageTarget(
        ctx.site,
        web.id,
        content_uri=containers.DataContainerUri,
        manifest_uri=containers.MetadataContainerUri,
        encryption_key=containers.EncryptionKey,
        list_title=library_title,
        list_url=library_url,
        web_url=web_url,
    )
    job = MigrationJob(FileSystemSource(args.source), target)

    print("Planning…", flush=True)
    print(f"Planned {len(job.plan())} files/folders")

    print("Packaging + submitting…", flush=True)
    job.run()
    print(f"Ingestion job submitted: {target.job_id}")

    # 5. Monitor until the job is terminal.
    print("Monitoring…", flush=True)
    print(f"Final status: {target.monitor(interval=args.interval, progress=on_progress)}")


if __name__ == "__main__":
    main()
