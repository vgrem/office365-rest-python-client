"""
Provision a project workspace in one idempotent pass.

A cross-domain "new project" setup that stitches together a document library
with typed metadata columns, a task list with a custom view, and a few starter
rows. It is safe to run repeatedly: lists and fields are ensured
(get-or-create), views are created only when missing, and starter rows are
seeded only while the task list is empty.

    python provision_project_workspace.py
    python provision_project_workspace.py --doc-library "Project Files" --task-list "Project Tasks"

Requires ``Sites.ReadWrite.All`` or an owner-level account on the target site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from __future__ import annotations

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.fields.creation_information import FieldCreationInformation
from office365.sharepoint.fields.type import FieldType
from office365.sharepoint.lists.templates.type import ListTemplateType
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

#: Library column -> (type, choices) — choices only for Choice fields.
DOC_LIBRARY_FIELDS = {
    "ProjectStage": (FieldType.Choice, ["Discovery", "In Progress", "Review", "Done"]),
    "Budget": (FieldType.Number, None),
    "ClientDueDate": (FieldType.DateTime, None),
}

#: Task list column -> (type, choices).
TASK_FIELDS = {
    "Status": (FieldType.Choice, ["Not Started", "In Progress", "Blocked", "Done"]),
    "Owner": (FieldType.Text, None),
    "DueDate": (FieldType.DateTime, None),
}

SEED_TASKS = [
    {"Title": "Kickoff and scope", "Status": "Done", "Owner": "PM"},
    {"Title": "Collect requirements", "Status": "In Progress", "Owner": "BA"},
    {"Title": "Draft solution design", "Status": "Not Started", "Owner": "Architect"},
]


def ensure_fields(lst, spec: dict) -> list[str]:
    """Ensure every typed column in ``spec`` exists on ``lst``; return internal names."""
    fields = []
    for title, (field_type, choices) in spec.items():
        info = FieldCreationInformation(Title=title, FieldTypeKind=field_type)
        if choices:
            info.Choices = list(choices)
        fields.append(lst.fields.ensure(info))
    lst.context.execute_query()
    return [f.internal_name for f in fields]


def main() -> None:
    parser = argparse.ArgumentParser(description="Provision a project workspace (library, task list, views, seed rows)")
    parser.add_argument("--doc-library", default="Project Files", help="document library title")
    parser.add_argument("--task-list", default="Project Tasks", help="task list title")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    web = ctx.web.get().execute_query()
    print(f"Site: {web.title} ({web.url})\n")

    # 1. Document library with typed metadata columns and a by-stage view.
    library = ctx.web.lists.ensure_list(
        args.doc_library,
        description="Project deliverables and working documents",
        template_type=ListTemplateType.DocumentLibrary,
        on_conflict="update",
    ).execute_query()
    doc_fields = ensure_fields(library, DOC_LIBRARY_FIELDS)
    library.views.ensure_view("By stage", fields=["Title", "ProjectStage", "ClientDueDate", "Budget"]).execute_query()
    print(f"Library  : {library.title}  (columns: {', '.join(doc_fields)}, view: By stage)")

    # 2. Task list with typed columns and a view.
    tasks = ctx.web.lists.ensure_list(
        args.task_list,
        description="Track project tasks",
        template_type=ListTemplateType.GenericList,
        on_conflict="update",
    ).execute_query()
    task_fields = ensure_fields(tasks, TASK_FIELDS)
    tasks.views.ensure_view("Open tasks", fields=["Title", "Status", "Owner", "DueDate"]).execute_query()
    print(f"Task list: {tasks.title}  (columns: {', '.join(task_fields)}, view: Open tasks)")

    # 3. Seed starter rows once, so re-runs stay idempotent.
    if not tasks.items.get().execute_query():
        for row in SEED_TASKS:
            tasks.add_item(row)
        ctx.execute_query()
        print(f"Seeded   : {len(SEED_TASKS)} starter task(s)")
    else:
        print("Seeded   : task list already has rows (nothing to do)")

    print(f"\nWorkspace ready at {web.url}/{args.doc_library}")


if __name__ == "__main__":
    main()
