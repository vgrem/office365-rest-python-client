"""
Auto-apply a retention label to unlabeled files across all SharePoint sites.

Lifecycle:
  1. CREATE a retention label (via security.labels.retention_labels.add)
  2. DISCOVER all SharePoint sites (via sites.get_all_sites)
  3. SCAN each site's default document library for files
  4. CHECK existing retention label on each file
  5. APPLY the label if the file is unlabeled and within retention window
  6. REPORT files labeled, skipped (too old, existing), errors

Requires Role: Global Administrator or Compliance Administrator
Requires delegated permissions:
  RecordsManagement.ReadWrite.All  (create label)
  Sites.ReadWrite.All               (enumerate sites, read/update items)
"""

import sys
from datetime import datetime, timedelta

from office365.directory.permissions.guard import has_role
from office365.directory.security.labels.retention.actionafterretentionperiod import (
    ActionAfterRetentionPeriod,
)
from office365.directory.security.labels.retention.behaviorduringretentionperiod import (
    BehaviorDuringRetentionPeriod,
)
from office365.directory.security.labels.retention.defaultrecordbehavior import (
    DefaultRecordBehavior,
)
from office365.directory.security.labels.retention.duration_in_days import (
    RetentionDurationInDays,
)
from office365.directory.security.labels.retention.trigger import RetentionTrigger
from office365.graph_client import GraphClient
from tests import test_admin_principal_name, test_client_id, test_tenant

LABEL_NAME = "Auto-Retain-365D"
RETENTION_DAYS = 365


def auth_client():
    """Authenticate with interactive browser flow (delegated)."""
    client = GraphClient(tenant=test_tenant).with_token_interactive(test_client_id, test_admin_principal_name)
    if not (has_role(client, "Global Administrator") or has_role(client, "Compliance Administrator")):
        print("This script requires Global Administrator or Compliance Administrator role.")
        sys.exit(1)
    return client


def create_label(client):
    """Create a retention label if it doesn't already exist."""
    try:
        label = client.security.labels.retention_labels.add(
            LABEL_NAME,
            RetentionTrigger.dateLabeled,
            RetentionDurationInDays(RETENTION_DAYS),
            BehaviorDuringRetentionPeriod.retainAsRecord,
            DefaultRecordBehavior.startLocked,
            ActionAfterRetentionPeriod.delete,
        ).execute_query()
        print(f"[OK] Label created: {label.display_name}")
        return label
    except Exception as e:
        if "nameAlreadyExists" in str(e):
            print(f"[~] Label '{LABEL_NAME}' already exists, reusing.")
            return None
        raise


def scan_and_apply_labels(client):
    """Iterate all sites, scan files, apply label to unlabeled items."""
    cutoff = datetime.utcnow() - timedelta(days=RETENTION_DAYS)
    stats = {"sites": 0, "drives": 0, "files": 0, "labeled": 0, "errors": 0}

    all_sites = client.sites.get_all_sites().execute_query()
    print(f"\nFound {len(all_sites)} sites. Scanning for unlabeled files...\n")

    for site in all_sites:
        stats["sites"] += 1
        try:
            drives = site.drives.get().execute_query()
        except Exception:
            continue

        for drive in drives:
            if any(x in (drive.name or "") for x in ["Preservation Hold", "Wiki Data", "App Catalog"]):
                continue
            stats["drives"] += 1

            try:
                items = drive.root.children.get().execute_query()
            except Exception:
                continue

            for item in items:
                stats["files"] += 1
                if not item.file:
                    continue

                try:
                    item.retention_label.get().execute_query()
                    if item.retention_label.name:
                        continue

                    created = item.created_datetime
                    if created and created > cutoff:
                        item.set_retention_label(LABEL_NAME).execute_query()
                        stats["labeled"] += 1
                        print(f"  + {site.display_name} / {drive.name} / {item.name}")
                    else:
                        print(f"  - {site.display_name} / {drive.name} / {item.name} (created {created}, too old)")
                except Exception as e:
                    stats["errors"] += 1
                    print(f"  ! {site.display_name} / {drive.name} / {item.name} — {e}")

    return stats


def main():
    client = auth_client()
    create_label(client)
    stats = scan_and_apply_labels(client)

    print(f"\n{'=' * 50}")
    print("Summary:")
    print(f"  Sites scanned:  {stats['sites']}")
    print(f"  Drives scanned: {stats['drives']}")
    print(f"  Files checked:  {stats['files']}")
    print(f"  Labeled:        {stats['labeled']}")
    print(f"  Errors:         {stats['errors']}")


if __name__ == "__main__":
    main()
