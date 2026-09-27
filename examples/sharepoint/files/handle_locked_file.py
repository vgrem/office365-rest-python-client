"""
Handle a file that is locked because it is open for editing (HTTP 423).

A file open in Office (web or desktop) carries a *shared lock*. The API cannot
break that lock, so overwriting the content fails with ``SPFileLockedException``
(HTTP 423). This example shows the supported strategies:

1. retry until the editing session closes and the lock is released,
2. delete with ``bypass_shared_lock=True`` (an explicit opt-in).

To change only the item metadata while the file is open, the REST API exposes
``ListItem.update_ex(bypass_shared_lock=True)``.

See https://github.com/vgrem/office365-rest-python-client/issues/697
"""

import argparse

from office365.runtime.exceptions import FileLockedException
from office365.runtime.retry import retry_on
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.exceptions import SPFileLockedException
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Work with a file that may be open/locked")
    parser.add_argument("--file-url", default="Shared Documents/Financial Sample.xlsx", help="server-relative URL")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    file = ctx.web.get_file_by_server_relative_url(args.file_url)

    # 1) Replace the content, retrying while the file is open elsewhere.
    #    A shared lock is released once the other session closes.
    try:
        with open("../../data/Financial Sample.xlsx", "rb") as f:
            file.save_binary_stream(f.read()).execute_query_retry(
                max_retry=3, is_retriable=retry_on(FileLockedException)
            )
        print("Content replaced")
    except SPFileLockedException as ex:
        print(f"Still locked by: {ex.lock_owner or 'another user'}")
        print(ex.GUIDANCE)

    # 2) Deleting is an explicit opt-in to bypass the shared lock.
    # file.delete_object(bypass_shared_lock=True).execute_query()


if __name__ == "__main__":
    main()
