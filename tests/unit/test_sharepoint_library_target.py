"""Offline tests for the document-library adapters, driven over a scripted transport.

Each test gets a real ``ClientContext`` whose transport answers by URL, so the objects
under test are the real ``Folder``/``File``/``ListItem`` models. What these tests pin is
the request the client sends — the endpoint, the projection, the form values — and what it
parses back, not a stand-in's method calls.

The library adapters are the one part of the migration framework a tenant run cannot check
for you: an E2E test writes a file and reads it, while these carry the things a single-pass
copy loses —

* the target enumeration skips SharePoint-owned scaffolding (``Forms/``, ``desktop.ini``,
  and on ``SiteAssets`` the site icon and the auto-provisioned ``<web title> Notebook``),
  or every migrated library is reported as having extra content;
* timestamps are converted to the web's wall clock once per value and land in a single
  system update, with the authorship values folded in so ``Editor`` is not reset;
* a folder is a list item: its own column values and system metadata round-trip;
* a draft file's approval state is carried, and its history is read oldest-first by
  version number (``1.10`` is newer than ``1.9``, which a text sort gets backwards).
"""

from __future__ import annotations

from office365.migration.base import MigrationItem, Principal
from office365.migration.sharepoint.adapters import SharePointLibrarySource, SharePointLibraryTarget
from office365.sharepoint.client_context import ClientContext
from tests._scripted_transport import RoutingTransport

_SITE_URL = "https://contoso.sharepoint.com/sites/x"
_DOCS = "/sites/x/Docs"
_FILE_URL = f"{_DOCS}/doc.txt"
_LOGIN = "i:0#.f|membership|vgrem@x.onmicrosoft.com"


# ── The scripted library ─────────────────────────────────────────────────────


def _web_payload(**extra):
    payload = {
        "__metadata": {"type": "SP.Web"},
        "ServerRelativeUrl": "/sites/x",
        "Title": "Project",  # the SiteAssets notebook rule names the folder after it
        "RegionalSettings": {
            "__metadata": {"type": "SP.RegionalSettings"},
            "TimeZone": {"__metadata": {"type": "SP.TimeZone"}, "Description": "UTC"},
        },
    }
    payload.update(extra)
    return {"d": payload}


def _file_payload(**extra):
    payload = {
        "__metadata": {"type": "SP.File"},
        "ServerRelativeUrl": _FILE_URL,
        "Length": "4",
        "ListItemAllFields": {"__metadata": {"type": "SP.ListItem"}, "Id": "1"},
    }
    payload.update(extra)
    return {"d": payload}


def _folder_payload(url=_DOCS, **extra):
    payload = {"__metadata": {"type": "SP.Folder"}, "ServerRelativeUrl": url, "Exists": True}
    payload.update(extra)
    return {"d": payload}


def _listing(kind: str, *urls, **extra):
    """A ``Files``/``Folders`` listing, as verbose JSON returns it."""
    return {
        "d": {"results": [{"__metadata": {"type": f"SP.{kind}"}, "ServerRelativeUrl": url, **extra} for url in urls]}
    }


def _files(*urls, **extra):
    return _listing("File", *urls, **extra)


def _folders(*urls, **extra):
    return _listing("Folder", *urls, **extra)


def _paged(*pages):
    """A listing route serving one page per read and an empty page after the last.

    A library read pages until a page comes back empty, so a single static page would
    be read forever.
    """
    remaining = [*pages]
    return lambda _request: remaining.pop(0) if remaining else {"d": {"results": []}}


def _moderated(status: int = 1) -> dict:
    """A file's list item as the approval-state projection returns it."""
    return {"d": {"__metadata": {"type": "SP.ListItem"}, "Id": "1", "OData__ModerationStatus": status}}


def _list_payload(**extra):
    payload = {
        "__metadata": {"type": "SP.List"},
        "Title": "Docs",
        "BaseTemplate": 101,
        "ItemCount": 1,
        "EnableModeration": True,  # approval state is only read on a moderating library
    }
    payload.update(extra)
    return {"d": payload}


def _updated(*fields):
    """A ``ValidateUpdateListItem`` response: the values the service accepted."""
    return {
        "d": {
            "ValidateUpdateListItem": {
                "results": [
                    {
                        "__metadata": {"type": "SP.ListItemFormUpdateValue"},
                        "FieldName": name,
                        "FieldValue": value,
                        "ErrorCode": 0,
                        "HasException": False,
                    }
                    for name, value in fields
                ]
            }
        }
    }


def _context(*extra, **routes) -> ClientContext:
    """A real context over the routes a library call makes.

    ``routes`` names the ones a test cares about and keeps the default for the rest;
    ``extra`` adds a route the defaults cannot express (a per-value answer). The order
    below is most-specific-key-first, because a route matches on a URL substring.
    """
    web = routes.get("web", _web_payload())
    entries = {"d": {"results": []}}
    return _context_with(
        [
            *extra,
            ("Files/add", routes.get("upload", {"d": {"ServerRelativeUrl": f"{_DOCS}/a.txt", "Length": "4"}})),
            ("Folders/add", routes.get("ensure", {"d": {"ServerRelativeUrl": f"{_DOCS}/Area1"}})),
            ("ValidateUpdateListItem", routes.get("update", _updated())),
            ("UTCToLocalTime", routes.get("conversion", {"d": {"UTCToLocalTime": "2021-06-01T15:00:00"}})),
            ("OpenBinaryStream", routes.get("stream", b"bytes")),
            ("versions", routes.get("versions", entries)),
            (
                "EnsureUser",
                routes.get("ensureuser", {"d": {"__metadata": {"type": "SP.User"}, "Id": 9, "LoginName": _LOGIN}}),
            ),
            # a listing URL sits under ``getFolderByServerRelativePath(...)``, and the
            # recursive walk revisits each subfolder, so the collection keys come first
            ("Folders(<key>)", entries),
            (")/Files", routes.get("files", entries)),
            (")/Folders", routes.get("folders", entries)),
            (")/Items", routes.get("items", entries)),
            (")/items", routes.get("items", entries)),
            (")/Fields", routes.get("fields", entries)),
            ("ItemAllFields", routes.get("moderation", _moderated())),
            ("GetByTitle", routes.get("list", _list_payload())),
            ("getFileByServerRelativeUrl", routes.get("file", _file_payload())),
            ("getFolderByServerRelativePath", routes.get("folder", _folder_payload())),
            ("RegionalSettings", web),
            ("/_api/Web", web),
        ]
    )


def _context_with(routes) -> ClientContext:
    ctx = ClientContext(_SITE_URL)
    ctx.pending_request().beforeExecute.clear()
    ctx.pending_request().transport = RoutingTransport(routes)
    return ctx


def _folder(ctx: ClientContext, url: str = _DOCS):
    folder = ctx.web.get_folder_by_server_relative_path(url)
    folder.set_property("ServerRelativeUrl", url)
    return folder


def _target(ctx: ClientContext, **kwargs) -> SharePointLibraryTarget:
    return SharePointLibraryTarget(_folder(ctx), **kwargs)


def _list(ctx: ClientContext):
    """The target library as a list, for the folder-record path."""
    return ctx.web.lists.get_by_title("Docs")


def _requests(ctx: ClientContext) -> list:
    return ctx.pending_request().transport.requests


def _file_item(**extra) -> MigrationItem:
    values = {"source_path": "/sites/src/doc.txt", "dest_path": "doc.txt", "item_type": "file"}
    values.update(extra)
    return MigrationItem(**values)


def _folder_item(dest_path: str = "Area1/") -> MigrationItem:
    return MigrationItem(source_path=f"/sites/src/{dest_path}", dest_path=dest_path, item_type="folder")


# ── Writing ──────────────────────────────────────────────────────────────────


def test_a_file_is_uploaded_to_the_library_and_costs_one_request():
    ctx = _context()

    _target(ctx).write(MigrationItem("/sites/src/a.txt", "a.txt"), b"data")

    (request,) = _requests(ctx)  # no folder-ensure round trip for a plain file
    assert request.method.value == "POST"
    assert request.url.endswith(
        f"getFolderByServerRelativePath(DecodedUrl='{_DOCS}')/Files/add(overwrite=true,url='a.txt')"
    )
    assert request.data == b"data"


def test_a_folders_checksum_is_the_empty_hash_not_a_content_hash():
    # A folder has no bytes; without the target list its values are unknown, and an
    # unknown value must not compare equal to a migrated one.
    target = _target(_context())

    assert target.checksum(_folder_item("a/")) == "" == target.checksum(_folder_item("b/"))


# ── Target enumeration (what verification must not report as extra) ───────────


def test_list_paths_skips_site_assets_scaffolding():
    ctx = _context(
        web=_web_payload(Title="Project"),
        files=_paged(_files("/sites/x/SiteAssets/__siteIcon__.png", "/sites/x/SiteAssets/logo.png")),
        # a folder's URL carries no trailing slash; the migration path adds it
        folders=_folders(
            "/sites/x/SiteAssets/Project Notebook",
            "/sites/x/SiteAssets/Images",
            "/sites/x/SiteAssets/Forms",
        ),
    )
    target = SharePointLibraryTarget(_folder(ctx, "/sites/x/SiteAssets"))

    assert target.list_paths() == ["logo.png", "Images/"]


# ── Timestamps (web-local conversion, one system update) ─────────────────────


def test_a_timestamp_conversion_is_requested_once_per_distinct_value():
    ctx = _context()
    target = _target(ctx)
    item = _file_item(created="2021-06-01T15:00:00+00:00", modified="2021-06-01T15:00:00+00:00")

    target.apply_timestamps(item)
    target.apply_timestamps(item)

    conversions = [request for request in _requests(ctx) if "UTCToLocalTime" in request.url]
    assert len(conversions) == 1  # the second call answered from the cache


def test_authorship_rides_along_in_the_timestamp_update():
    ctx = _context(
        ("datetime'2022-07-02T16:00:00'", {"d": {"UTCToLocalTime": "2022-07-02 16:00:00"}}),
        ("datetime'2021-06-01T15:00:00'", {"d": {"UTCToLocalTime": "2021-06-01 15:00:00"}}),
    )
    target = _target(ctx)
    item = _file_item(created="2021-06-01T15:00:00+00:00", modified="2022-07-02T16:00:00+00:00")
    item.author = Principal(_LOGIN, "1", "Vadim")

    target.apply_authorship(item)
    assert [r for r in _requests(ctx) if "ValidateUpdateListItem" in r.url] == []  # nothing written yet

    target.apply_timestamps(item)

    (update,) = [request for request in _requests(ctx) if "ValidateUpdateListItem" in request.url]
    form = {entry["FieldName"]: entry["FieldValue"] for entry in update.data["formValues"]}
    assert form["Created"] == "2021-06-01 15:00:00"  # wall clock, with datesInUTC below
    assert form["Modified"] == "2022-07-02 16:00:00"
    assert form["Author"] == "[{'Key':'i:0#.f|membership|vgrem@x.onmicrosoft.com'}]"
    assert update.data["datesInUTC"] is True
    assert update.data["bNewDocumentUpdate"] is True  # a system update: no extra version


# ── Folder values (a folder is a list item too) ──────────────────────────────


def test_a_folder_value_the_service_rejects_is_reported_not_fatal():
    ctx = _context(update=("deny",))
    target = _target(ctx, sp_list=_list(ctx))

    target.write(_folder_item("Area1/"), {"Region": "North"})

    assert any("folder column values for 'Area1/'" in warning for warning in target.warnings)


def test_a_folders_metadata_reads_back_from_the_folder_resource():
    # The timestamp write lands on the folder's list item; the folder resource reports
    # the same instant, and it is what the source side reads too.
    created, modified = "2021-03-04T05:06:07Z", "2021-03-05T06:07:08Z"
    ctx = _context(folder=_folder_payload(f"{_DOCS}/Area1", TimeCreated=created, TimeLastModified=modified))

    metadata = _target(ctx).read_metadata(_folder_item("Area1/"))

    assert metadata == {"created": "2021-03-04T05:06:07+00:00", "modified": "2021-03-05T06:07:08+00:00"}


# ── Approval state ───────────────────────────────────────────────────────────


def _source(ctx: ClientContext) -> SharePointLibrarySource:
    return SharePointLibrarySource(_folder(ctx), sp_list=_list(ctx))


def _sourced(**routes) -> tuple[SharePointLibrarySource, ClientContext]:
    """The same library read as a source, with the approval state a draft carries."""
    routes.setdefault("files", _paged(_files(_FILE_URL)))
    routes.setdefault(
        "items",
        {
            "d": {
                "results": [
                    {
                        "__metadata": {"type": "SP.ListItem"},
                        "FileRef": _FILE_URL,
                        "OData__ModerationStatus": 0,
                        "OData__ModerationComments": "wip",
                    }
                ]
            }
        },
    )
    ctx = _context(**routes)
    return _source(ctx), ctx


def test_a_draft_files_approval_state_is_read_with_its_comments():
    # Only a draft/pending or rejected file needs its state carried; an uploaded file
    # starts out approved. The state rides in the author-id read, so the verification
    # diff sees it without a round trip of its own.
    source, ctx = _sourced()
    item = source.list_items()[0]

    assert source.read_item_state(item) == {"_ModerationStatus": "0", "_ModerationComments": "wip"}
    assert source.read_metadata(item)["moderation_status"] == "0"
    (read,) = [request for request in _requests(ctx) if "HasUniqueRoleAssignments" in request.url]
    assert "OData__ModerationStatus" in read.url  # projected on a moderating library


def test_the_written_approval_state_is_a_separate_system_update():
    # A document rejects a moderation change combined with other properties, so this
    # write cannot ride along with the timestamps; ``_ModerationStatus`` is the field
    # name ``ValidateUpdateListItem`` accepts for the OData-escaped column.
    ctx = _context()

    _target(ctx).apply_item_state(_file_item(), {"_ModerationStatus": "1", "_ModerationComments": "wip"})

    (update,) = [request for request in _requests(ctx) if "ValidateUpdateListItem" in request.url]
    assert [(entry["FieldName"], entry["FieldValue"]) for entry in update.data["formValues"]] == [
        ("_ModerationStatus", "1"),
        ("_ModerationComments", "wip"),
    ]
    assert update.data["bNewDocumentUpdate"] is True


def test_a_written_files_approval_state_reads_back_through_the_projection():
    # The written state is read back off the file's list item, projected to the one
    # column: a library without moderation has no such column, and the diff must not
    # fail over it.
    ctx = _context()

    metadata = _target(ctx).read_metadata(_file_item())

    assert metadata["moderation_status"] == "1"
    (read,) = [request for request in _requests(ctx) if "ItemAllFields" in request.url]
    assert "$select=OData__ModerationStatus" in read.url


# ── History (the draft hides its published predecessor) ──────────────────────


def test_version_history_is_oldest_first_by_number_without_the_current_version():
    # Live shape on a 13-version document: every version comes back, the current content
    # included, and a label is ``major.minor`` — so comparing labels as text puts "1.10"
    # before "1.9".
    versions = [
        {"__metadata": {"type": "SP.FileVersion"}, "VersionLabel": label, "IsCurrentVersion": current}
        for label, current in (("1.10", False), ("1.11", True), ("1.9", False))
    ]
    ctx = _context(
        files=_paged(_files(_FILE_URL, UIVersionLabel="1.11")),
        versions={"d": {"results": versions}},
        stream=_paged(b"bytes of 1.9", b"bytes of 1.10"),
    )
    source = _source(ctx)

    current, older = source.read_version_history(source.list_items()[0])

    assert current == "1.11"
    # the current version's bytes are the file's content, which read() already supplies
    assert older == [("1.9", b"bytes of 1.9"), ("1.10", b"bytes of 1.10")]
