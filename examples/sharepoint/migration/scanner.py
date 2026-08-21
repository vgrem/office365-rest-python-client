"""
Run a site migration assessment scan using the SharePoint Migration API.

Requires read access to the target site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/migration-api-reference
"""

import argparse
import logging

from office365.migration.assessor import MigrationAssessor
from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username

logging.basicConfig(level=logging.INFO)


def main():
    argparse.ArgumentParser(description="Run a site migration assessment").parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    report = MigrationAssessor(ctx.web).include_permissions().include_versions().assess().execute_query()

    print(report.value.summary())
    print(report.value.blockers)


if __name__ == "__main__":
    main()
