"""
SPMT-style migration — a registered session with tasks, run like the cmdlets.

Mirrors ``Microsoft.SharePoint.MigrationTool.PowerShell``:

    Register-SPMTMigration    -> session.register(...)
    Add-SPMTTask              -> session.add_task(...)
    Show-SPMTMigration        -> session.show()
    Start-SPMTMigration       -> session.start()
    Stop-SPMTMigration        -> session.stop()
    Unregister-SPMTMigration  -> session.unregister()

By default tasks upload over REST; pass ``--migration-api`` to package + ingest
server-side (the SPMT path — full fidelity, needs the ``[azure]`` extra).

    python migrate_spmt.py                       # examples/data -> Documents
    python migrate_spmt.py --migration-api

Requires: write access to the target library (and, for ``--migration-api``, an app
with the ``Sites.FullControl.All`` application permission).
"""

from __future__ import annotations

import argparse
from pathlib import Path

from office365.migration import MigrationSession, MigrationSettings
from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="SPMT-style migration session")
    parser.add_argument("--source", default="../../../data", help="local folder (default: examples/data)")
    parser.add_argument("--library", default="Documents", help="target library title")
    parser.add_argument("--migration-api", action="store_true", help="use the server-side Migration API")
    args = parser.parse_args()

    source = Path(args.source)
    if not source.is_dir():
        parser.error(f"not a directory: {source} — run this script from its own folder")

    ctx = ClientContext(site_url).with_client_certificate(tenant, client_id, cert_thumbprint, cert_path)

    # Register-SPMTMigration — the session settings + the target context
    session = MigrationSession().register(
        context=ctx,
        settings=MigrationSettings(use_migration_api=args.migration_api),
    )

    # Add-SPMTTask — a file-share task (a local folder -> a library)
    session.add_task(
        file_share_source=str(source),
        target_site_url=site_url,
        target_list=args.library,
    )

    # Start-SPMTMigration
    print("Migrating…", flush=True)
    for status in session.start():
        stats = status["stats"]
        print(
            f"  [{status['phase']}] {status['source']} -> {status['target']} "
            f"success={stats['success']} skipped={stats['skipped']} errors={stats['errors']}"
        )

    # Show-SPMTMigration
    for status in session.show():
        print(f"  task {status['id']}: {status['phase']}")

    # Unregister-SPMTMigration
    session.unregister()


if __name__ == "__main__":
    main()
