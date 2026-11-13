"""Build the M0 fixture surface — a library, a list and a site — idempotently.

Plan 00 §1.1 asks for a *source* able to settle the step 1.4 questions, and the two
tenant runs of 2026-11-13 could not settle any of them: they were made against
existing lists, with no versions, no unique permissions and no pages. This script
creates what those questions need, and does nothing else:

| fixture                        | the step 1.4 question it answers                            |
| ------------------------------ | ----------------------------------------------------------- |
| library, ``--versions`` each   | per-version author and time on both paths                    |
| one file checked out           | a checked-out file is not silently copied or silently failed |
| folder with unique permissions | group principals and ACL travel through the server-side path |
| list, every column type        | a non-library list through the server-side path              |
| person + lookup values on item | typed values survive, instead of arriving as strings         |
| site group, custom permission  | an ACL names a principal that exists only on the target      |
| subweb, modern + wiki page     | the site scope has a page and a child web to lose            |
| quick-launch node              | navigation is compared, not just counted                     |

It is **idempotent**: every object is looked up first and reused, so a second run
is a read of what the first one built. Nothing is ever deleted except with
``--delete``, which removes the whole fixture site and nothing else.

    python build_fixture_site.py                  # print the surface; sends nothing
    python build_fixture_site.py --apply          # create what is missing, reuse the rest
    python build_fixture_site.py --apply --delete  # remove the fixture site again

The fixture is a **site collection** at ``{root}/sites/m0-fixture``, created through
the tenant admin endpoint. It began life as a subweb of ``OFFICE365_SITE_URL`` and
the tenant refused it: *you cannot customize permission levels in a web site with
inherited permission levels* — role definitions are site-collection scoped. That
refusal is also the finding recorded as F3 in ``11b-observed-results.md``: a
subsite cannot carry the site-scope surface, so a site collection is the target
M0 actually needs.

Offline measurement: an upload costs ~1.4 s single-threaded (0.69 files/s, run D),
so the default 6 files x 5 versions is ~45 s and ``--files 1000`` is ~2.4 h. The
default stays small on purpose: the fixture proves the *shape*, the volume run is
what ``--files 1000`` is for.

Requires the ``.env`` credentials the other migration examples use, and
**Sites.FullControl.All** — creating a site collection, a role definition and a
site group is tenant administration, not a content write.
"""

from __future__ import annotations

import argparse
import http
import json
import time
from typing import Any, Callable
from urllib.parse import urlparse
from uuid import uuid4

from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.exceptions import ObjectNotFoundException
from office365.runtime.retry import is_transient_error
from office365.sharepoint.attachments.creation_information import AttachmentCreationInformation
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.fields.lookup_value import FieldLookupValue
from office365.sharepoint.fields.user_value import FieldUserValue
from office365.sharepoint.lists.templates.type import ListTemplateType
from office365.sharepoint.navigation.nodes.creationinformation import NavigationNodeCreationInformation
from office365.sharepoint.pages.template_file_type import TemplateFileType
from office365.sharepoint.permissions.base_permissions import BasePermissions
from office365.sharepoint.permissions.kind import PermissionKind
from office365.sharepoint.tenant.administration.tenant import Tenant
from office365.sharepoint.webs.creation_information import WebCreationInformation
from tests.settings import (
    admin_site_url,
    admin_username,
    cert_path,
    cert_thumbprint,
    client_id,
    root_site_url,
    tenant,
)

SITE_NAME = "m0-fixture"
SITE_URL = f"{root_site_url.rstrip('/')}/sites/{SITE_NAME}"
SITE_TITLE = "M0 fixture"
#: A site created without a template comes out classic, and a classic site has no
#: Site Pages library, so ``add_site_page`` refuses it. ``STS#3`` is the modern team site.
SITE_TEMPLATE = "STS#3"
SUBWEB = "sub"
LIBRARY = "M0 Library"
ITEMS = "M0 Items"
WIKI = "M0 Wiki"
GROUP = "M0 Fixture Readers"
ROLE = "M0 Contribute Lite"
MODERN_PAGE = "FixtureModern.aspx"
WIKI_PAGE = "WikiHome.aspx"
CHECKED_OUT = "f000.txt"
PROVISION_ATTEMPTS = 24  # a site collection answers 404 for a minute or two after the create is queued
PROVISION_SECONDS = 5
CANVAS = json.dumps([{"position": 1, "controlType": 4, "id": str(uuid4()), "innerHTML": "<p>M0 fixture</p>"}])


#: ``(title, how to add it)`` — the library's own columns, one per simple type.
LIBRARY_COLUMNS: tuple[tuple[str, Callable[[Any], Any]], ...] = (
    ("M0 Text", lambda fields: fields.add_text_field("M0 Text")),
    ("M0 Number", lambda fields: fields.add_number("M0 Number")),
    ("M0 Date", lambda fields: fields.add_datetime("M0 Date")),
    ("M0 Note", lambda fields: fields.add_note("M0 Note")),
    ("M0 Url", lambda fields: fields.add_url_field("M0 Url")),
    ("M0 Choice", lambda fields: fields.add_choice_field("M0 Choice", ["alpha", "beta"], True)),
)


def _item_columns(lst: Any) -> tuple[tuple[str, Callable[[Any], Any]], ...]:
    """Every typed column the migration maps — person, multi-choice and a lookup.

    The lookup points at the list itself, which is why the column table is a
    function: the field needs the list's id, and only the handle has it.
    """
    return (
        ("M0 Flag", lambda fields: fields.add_choice_field("M0 Flag", ["red", "green", "blue"])),
        ("M0 Tags", lambda fields: fields.add_choice_field("M0 Tags", ["one", "two"], True)),
        ("M0 Owner", lambda fields: fields.add_user_field("M0 Owner")),
        ("M0 Person", lambda fields: fields.add_user_field("M0 Person")),
        ("M0 Text", lambda fields: fields.add_text_field("M0 Text")),
        ("M0 Lookup", lambda fields: fields.add_lookup_field("M0 Lookup", lst, "Title")),
    )


_rows: list[tuple[str, str, str]] = []


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the M0 fixture surface (idempotent)")
    parser.add_argument("--admin-site", default=admin_site_url, help="the tenant admin endpoint")
    parser.add_argument("--owner", default=admin_username, help="site collection owner (a login name)")
    parser.add_argument("--files", type=int, default=6, help="files in the library (default: 6)")
    parser.add_argument("--versions", type=int, default=5, help="versions per file (default: 5)")
    parser.add_argument("--items", type=int, default=3, help="items in the list (default: 3)")
    parser.add_argument("--apply", action="store_true", help="write to the tenant (default: print the surface)")
    parser.add_argument("--delete", action="store_true", help="remove the fixture site instead of building it")
    return parser.parse_args()


def _surface(args: argparse.Namespace) -> str:
    return (
        f"{SITE_URL}   ({SITE_TITLE})\n"
        f"  {LIBRARY}/   library, versioning on, {args.files} files x {args.versions} versions,"
        f" {CHECKED_OUT} checked out\n"
        f"    unique-perm/       unique role assignments, {GROUP} granted Read\n"
        f"    nested/deep/       two levels, for path mapping\n"
        f"  {ITEMS}/              list, {args.items} items, attachments on, first item carries a file\n"
        f"  {WIKI}/               wiki page library, {WIKI_PAGE}\n"
        f"  SitePages/            {MODERN_PAGE} (modern, published)\n"
        f"  {SUBWEB}/              child web\n"
        f"  navigation            quick-launch node 'M0 fixture'\n"
        f"  permissions           group '{GROUP}', level '{ROLE}'"
    )


def _client(url: str) -> ClientContext:
    """A context that retries a 404.

    For a minute or two after a site collection is created, SharePoint answers ``_api``
    calls at random with a 404 that the runtime calls permanent. Every probe in this
    script reads a 404 as "not there", so that answer has to be asked again — retrying
    it is safe for writes too, since the request never reached the collection.
    """
    return (
        ClientContext(url)
        .with_client_certificate(tenant, client_id, cert_thumbprint, cert_path)
        .with_auto_retry(is_retriable=_retriable)
    )


def _retriable(err: Exception) -> bool:
    response = getattr(err, "response", None)
    return is_transient_error(err) or (response is not None and response.status_code == http.HTTPStatus.NOT_FOUND)


def _exists(getter: Callable[[], Any]) -> bool:
    """True when the addressed object resolves — a refusal *is* the answer to a probe.

    The getter must queue a read: an addressed object that nothing has been asked of
    sends no request, so it would answer "exists" without the server being consulted.
    """
    try:
        getter().execute_query()
        return True
    except ClientRequestException:
        return False


def _names(collection: Any, prop: str = "Title") -> set[str]:
    return {getattr(item, prop.lower()) for item in collection.select([prop]).get().execute_query()}


def _site(args: argparse.Namespace) -> Any:
    """The fixture site collection, created through the tenant admin endpoint if absent."""
    web = _client(SITE_URL).web
    if _exists(lambda: web.get()):  # noqa: PLW0108 - the call must be deferred
        _rows.append(("reused", "site collection", SITE_URL))
        return web
    # ``create_site_sync`` cannot be used here: it rebases the admin context onto the
    # new site (``Site.set_property("__siteUrl")``) and then polls the admin endpoint
    # through it, which is a 500. Queue the create, then wait for the site to answer.
    try:
        Tenant(_client(args.admin_site)).create_site(SITE_URL, args.owner, SITE_TITLE, SITE_TEMPLATE).execute_query()
    except ObjectNotFoundException:
        # The probe above cannot tell "not there" from "not yet", so the create can be
        # refused with "a site already exists" — which is the site that was wanted.
        pass
    for _attempt in range(PROVISION_ATTEMPTS):
        if _exists(lambda: web.get()):  # noqa: PLW0108 - deferred on purpose
            _rows.append(("created", "site collection", SITE_URL))
            return web
        time.sleep(PROVISION_SECONDS)
    raise SystemExit(f"{SITE_URL} did not answer after {PROVISION_ATTEMPTS * PROVISION_SECONDS}s; rerun to continue")


def _list(web: Any, title: str, template: ListTemplateType) -> Any:
    """The list, created if missing. The handle is always re-read by title: a list
    returned by ``add_list`` addresses its children through a placeholder key."""
    if title in _names(web.lists):
        _rows.append(("reused", "list", title))
    else:
        web.lists.add_list(title, f"M0 fixture: {title}", template_type=template).execute_query()
        _rows.append(("created", "list", title))
    return web.lists.get_by_title(title)


def _columns(lst: Any, specs: tuple[tuple[str, Callable[[Any], Any]], ...]) -> None:
    missing = [(title, add) for title, add in specs if title not in _names(lst.fields)]
    if not missing:
        return
    # The list handle names itself in the report, so it has to be read in the batch below.
    lst.ensure_property("Title")
    for _title, add in missing:
        add(lst.fields)
    lst.context.execute_query()
    _rows.extend(("created", "column", f"{lst.title}:{title}") for title, _ in missing)


def _versioning(lst: Any) -> None:
    """Versioning on the library — a file's history is what ``--versions`` builds."""
    lst.ensure_properties(["EnableVersioning"]).execute_query()
    if lst.enable_versioning:
        return
    lst.set_property("EnableVersioning", True).update().execute_query()
    _rows.append(("enabled", "library", "versioning"))


def _attachments(lst: Any) -> None:
    """Attachments on the list — a document library has them and may not be configured."""
    lst.ensure_properties(["EnableAttachments"]).execute_query()
    if lst.enable_attachments:
        return
    lst.set_property("EnableAttachments", True).update().execute_query()
    _rows.append(("enabled", "list", "attachments"))


def _folders(root: Any, web: Any, *paths: str) -> dict[str, Any]:
    """The folder paths under the library root, created level by level, parent first.

    A folder returned by ``folders.add`` or by the listing carries a placeholder
    key, and ``GetByPath`` resolves a name but not a path — so a folder is created
    through its parent's collection and addressed by its server-relative url.
    """
    base = root.get().execute_query().server_relative_url
    for path in paths:
        directory, _, name = path.rpartition("/")
        collection = (
            root.folders if not directory else web.get_folder_by_server_relative_path(f"{base}/{directory}").folders
        )
        if name in {folder.name for folder in collection.select(["Name"]).get().execute_query()}:
            continue
        collection.add(name).execute_query()
        _rows.append(("created", "folder", path))
    return {path: web.get_folder_by_server_relative_path(f"{base}/{path}").get() for path in paths}


def _files(root: Any, args: argparse.Namespace, web: Any) -> None:
    """Files with real history: the create lands a version, each save adds one.

    Measured: ``upload_file`` twice in a row collapses into one version, while
    ``save_binary_stream`` advances exactly one — and one save in twelve still collapsed,
    so the loop counts the versions the server reports rather than trusting the writes.
    """
    present = _names(root.files, "Name")
    base = urlparse(web.url).path
    for index in range(args.files):
        name = f"f{index:03d}.txt"
        if name not in present:
            root.upload_file(name, f"{name} version 1\n").execute_query()
        file = web.get_file_by_server_relative_url(f"{base}/{LIBRARY}/{name}")
        versions = len(list(file.versions.select(["VersionLabel"]).get().execute_query()))
        while versions < args.versions:
            file.save_binary_stream(f"{name} version {versions + 1}\n".encode()).execute_query()
            versions = len(list(file.versions.select(["VersionLabel"]).get().execute_query()))
        _rows.append(("created" if name not in present else "reused", "file", f"{name} x{versions}"))


def _checkout(web: Any) -> None:
    """One file left checked out — a state a migration has to report rather than lose.

    A file taken from a folder listing carries a placeholder key, so it is addressed
    by its server-relative url instead of being reused as-is.
    """
    base = urlparse(web.url).path
    file = web.get_file_by_server_relative_url(f"{base}/{LIBRARY}/{CHECKED_OUT}").get().execute_query()
    if file.check_out_type not in (None, 2):  # 2 = CheckOutType.None in the SharePoint enum
        _rows.append(("reused", "check-out", file.name))
        return
    file.checkout().execute_query()
    _rows.append(("created", "check-out", file.name))


def _unique_permissions(folder: Any, web: Any, group: Any) -> None:
    """Break inheritance on one folder and grant the fixture group Read.

    A :class:`Folder` is not a ``SecurableObject``; its ACL hangs off the item
    fields, which is the object the assignment is made against.
    """
    # A plain read does not answer the flag: it is a facet, and costs a $select.
    securable = folder.list_item_all_fields.select(["HasUniqueRoleAssignments"]).get().execute_query()
    if securable.has_unique_role_assignments:
        _rows.append(("reused", "unique permissions", folder.name))
        return
    securable.break_role_inheritance(copy_role_assignments=False).execute_query()
    securable.add_role_assignment(group, web.role_definitions.get_by_name("Read")).execute_query()
    _rows.append(("created", "unique permissions", f"{folder.name} (Read -> {GROUP})"))


def _first_site_user(web: Any) -> Any:
    """A real member of the site, so the person column holds a principal and not a string.

    Only a claims user (``i:0#.f|membership|<upn>``) will do: the site's own users
    include SharePoint's built-in shares and role-manager principals.
    """
    users = list(web.site_users.select(["Id", "LoginName"]).get().execute_query())
    return next((user for user in users if "|membership|" in str(user.login_name)), None)


def _items(lst: Any, args: argparse.Namespace) -> Any:
    items = list(lst.items.select(["Id", "Title"]).get().execute_query())
    for index in range(len(items), args.items):
        items.append(lst.add_item({"Title": f"M0 item {index + 1}"}).execute_query())
        _rows.append(("created", "item", f"M0 item {index + 1}"))
    item = items[0]
    if not list(item.attachment_files.get().execute_query()):
        item.attachment_files.add(
            AttachmentCreationInformation(filename="attached.txt", content=b"fixture attachment\n")
        ).execute_query()
        _rows.append(("created", "attachment", f"item {item.id}"))
    return item


def _values(item: Any, web: Any, target: Any) -> None:
    """One lookup and one person value, so typed columns are not merely declared.

    A typed value is written under the column's ``InternalName``, not its title: a column
    created through the API is titled ``M0 Lookup`` and named ``M0_x0020_Lookup``, and the
    title is refused by the server. Whether a value is already there is asked of the
    companion id (``M0_x0020_LookupId``), which a plain item read returns.
    """
    names = {
        field.title: field.internal_name
        for field in target.fields.select(["Title", "InternalName"]).get().execute_query()
    }
    item.get().execute_query()
    others = [other for other in target.items.select(["Id"]).get().execute_query() if other.id != item.id]
    user = _first_site_user(web)
    writes: list[tuple[str, int, Any, str]] = []
    if others:
        writes.append(
            (
                names["M0 Lookup"],
                others[0].id,
                FieldLookupValue(LookupId=others[0].id),
                f"M0 Lookup -> item {others[0].id}",
            )
        )
    if user is not None:
        writes.append((names["M0 Person"], user.id, FieldUserValue.from_user(user), f"M0 Person -> {user.login_name}"))
    changed = [write for write in writes if item.properties.get(f"{write[0]}Id") != write[1]]
    if not changed:
        _rows.append(("reused", "value", ", ".join(write[0] for write in writes)))
        return
    for name, _id, value, _note in changed:
        item.set_property(name, value)
    item.update().execute_query()
    _rows.extend(("set", "value", write[3]) for write in changed)


def _wiki(web: Any) -> None:
    library = _list(web, WIKI, ListTemplateType.WebPageLibrary)
    root = library.root_folder
    if _exists(lambda: web.get_file_by_server_relative_url(f"{urlparse(web.url).path}/{WIKI}/{WIKI_PAGE}").get()):
        _rows.append(("reused", "page", WIKI_PAGE))
        return
    root.files.add_template_file(WIKI_PAGE, TemplateFileType.WikiPage).execute_query()
    _rows.append(("created", "page", f"{WIKI}/{WIKI_PAGE} (wiki)"))


def _modern_page(web: Any) -> None:
    """A modern page, published — a page left as a draft cannot be a navigation target."""
    items = web.get_list_by_title("Site Pages").items.select(["Id", "FileLeafRef"]).get().execute_query()
    page_id = next((item.id for item in items if item.properties.get("FileLeafRef") == MODERN_PAGE), None)
    if page_id is None:
        page_id = web.add_site_page(MODERN_PAGE, title="M0 modern page").execute_query().properties["Id"]
        _rows.append(("created", "page", f"{MODERN_PAGE} (modern)"))
    page = web.get_site_page_by_id(page_id).get().execute_query()
    if not str(page.properties.get("Version", "1.0")).startswith("0."):
        _rows.append(("reused", "page", MODERN_PAGE))
        return
    page.save_draft("M0 modern page", canvas_content=CANVAS).execute_query()
    page.publish().execute_query()
    _rows.append(("published", "page", MODERN_PAGE))


def _navigation(web: Any) -> None:
    quick_launch = web.navigation.quick_launch
    if "M0 fixture" in _names(quick_launch):
        _rows.append(("reused", "navigation", "quick launch"))
        return
    url = f"{urlparse(web.url).path}/SitePages/{MODERN_PAGE}"
    quick_launch.add(NavigationNodeCreationInformation(Title="M0 fixture", Url=url, IsExternal=False)).execute_query()
    _rows.append(("created", "navigation", "quick launch -> M0 fixture"))


def _group(web: Any) -> Any:
    if GROUP in _names(web.site_groups):
        _rows.append(("reused", "group", GROUP))
        return web.site_groups.get_by_name(GROUP)
    _rows.append(("created", "group", GROUP))
    web.site_groups.add(GROUP, "M0 fixture readers").execute_query()
    return web.site_groups.get_by_name(GROUP)


def _role_definition(web: Any) -> None:
    if ROLE in _names(web.role_definitions, "Name"):
        _rows.append(("reused", "permission level", ROLE))
        return
    # A custom level needs unique role definitions, which a web inheriting its
    # parent's permissions does not have; the fixture web is its own site.
    web.ensure_properties(["HasUniqueRoleAssignments"]).execute_query()
    if not web.has_unique_role_assignments:
        web.break_role_inheritance(copy_role_assignments=True, clear_sub_scopes=False).execute_query()
        _rows.append(("created", "unique permissions", SITE_NAME))
    permissions = BasePermissions()
    for kind in (
        PermissionKind.Open,
        PermissionKind.OpenItems,
        PermissionKind.ViewListItems,
        PermissionKind.AddListItems,
        PermissionKind.EditListItems,
        PermissionKind.DeleteListItems,
    ):
        permissions.set(kind)
    web.role_definitions.add(permissions, ROLE, "M0 fixture: read and edit items, no design", 200).execute_query()
    _rows.append(("created", "permission level", ROLE))


def _subweb(web: Any) -> None:
    children = web.webs.select(["Url"]).get().execute_query()
    if any(w.url.rstrip("/").rsplit("/", 1)[-1].lower() == SUBWEB for w in children):
        _rows.append(("reused", "web", SUBWEB))
        return
    web.webs.add(
        WebCreationInformation(Title="M0 subweb", Url=SUBWEB, WebTemplate="STS#0", UseSamePermissionsAsParentSite=True)
    ).execute_query()
    _rows.append(("created", "web", SUBWEB))


def _delete(args: argparse.Namespace) -> int:
    if not _exists(lambda: _client(SITE_URL).web.get()):  # noqa: PLW0108 - deferred on purpose
        print(f"nothing to delete: {SITE_URL} does not exist")
        return 0
    tenant = Tenant(_client(args.admin_site))
    tenant.remove_site_sync(SITE_URL).execute_query()
    # A collection waiting in the recycle bin blocks a create of the same url.
    tenant.remove_deleted_site(SITE_URL).execute_query()
    print(f"deleted {SITE_URL}")
    return 0


def main() -> int:
    args = _parse_args()
    print(_surface(args))
    if not args.apply:
        print("\nDry run — nothing was sent. Pass --apply to build it.")
        return 0
    if args.delete:
        return _delete(args)

    web = _site(args)
    group = _group(web)
    _role_definition(web)
    target = _list(web, ITEMS, ListTemplateType.GenericList)
    library = _list(web, LIBRARY, ListTemplateType.DocumentLibrary)
    _versioning(library)
    _columns(library, LIBRARY_COLUMNS)
    _columns(target, _item_columns(target))
    _attachments(target)

    root = library.root_folder
    folders = _folders(root, web, "unique-perm", "nested", "nested/deep")
    _files(root, args, web)
    _checkout(web)
    _unique_permissions(folders["unique-perm"], web, group)

    item = _items(target, args)
    _values(item, web, target)
    _wiki(web)
    _modern_page(web)
    _navigation(web)
    _subweb(web)

    width = max(len(kind) for _action, kind, _name in _rows)
    for action, kind, name in _rows:
        print(f"  {action:<9} {kind:<{width}}  {name}")
    created = sum(1 for action, _k, _n in _rows if action != "reused")
    print(f"\n{created} change(s), {len(_rows) - created} reused — {SITE_NAME} is ready to migrate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
