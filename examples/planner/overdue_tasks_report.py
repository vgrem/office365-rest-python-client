"""
Overdue Planner tasks report.

Enumerates all Planner plans and reports the tasks that are past their due
date and still not completed, grouped by assignee. Optionally lists tasks
due within the next N days.

Inspired by Get-OpenPlannerTasksAnalysis.ps1 and Report-ObsoletePlannerTasks.PS1
from Office 365 for IT Pros.

Requires delegated permissions ``Group.Read.All`` and ``Tasks.Read.All``.

https://learn.microsoft.com/en-us/graph/api/planner-list-plans
https://learn.microsoft.com/en-us/graph/api/planner-list-tasks
https://learn.microsoft.com/en-us/graph/api/resources/plannertask
"""

import argparse
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Tuple

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def _parse_datetime(value) -> Optional[datetime]:
    """Coerce a dueDateTime value (datetime or ISO string) to timezone-aware datetime."""
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    return None


def _assignees(task) -> List[str]:
    """Display names of the users a task is assigned to."""
    assignments = task.properties.get("assignments", {}) or {}
    return [a.get("displayName", "?") for a in assignments.values() if isinstance(a, dict)]


def _overdue_tasks(client: GraphClient, days_ahead: int) -> List[Tuple]:
    """Collect overdue and due-soon tasks across all plans."""
    now = datetime.now(timezone.utc)
    deadline = now + timedelta(days=days_ahead) if days_ahead > 0 else None
    rows = []

    for plan in client.planner.plans.get_all().execute_query():
        plan_title = plan.properties.get("title", "?")
        for task in plan.tasks.get().execute_query():
            due = _parse_datetime(task.properties.get("dueDateTime", None))
            if due is None:
                continue
            status = "overdue" if due < now else ("due soon" if deadline and due <= deadline else None)
            if status is None:
                continue
            rows.append(
                (
                    plan_title,
                    task.title or "?",
                    due,
                    ", ".join(_assignees(task)),
                    task.percent_complete,
                    status,
                )
            )
    rows.sort(key=lambda r: r[2])
    return rows


def main():
    parser = argparse.ArgumentParser(description="Overdue Planner tasks report")
    parser.add_argument("--days-ahead", type=int, default=0, help="also list tasks due within the next N days")
    args = parser.parse_args()

    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
    rows = _overdue_tasks(client, args.days_ahead)

    if not rows:
        print("No overdue or due-soon tasks found.")
        return

    for plan, title, due, assignees, percent, status in rows:
        print(f"[{status}] {plan} / {title}  due {due:%Y-%m-%d}  {percent}%  assignees: {assignees}")

    overdue = sum(1 for r in rows if r[5] == "overdue")
    print(f"\n{overdue} overdue, {len(rows) - overdue} due soon")


if __name__ == "__main__":
    main()
