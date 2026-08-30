"""Field-level scanner — columns that block or complicate a list migration."""

from __future__ import annotations

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner


class FieldScanner(BaseScanner):
    """Flags ReadOnly fields, system approval-workflow fields, and schema attrs."""

    category = "field"

    def run(self, fields, report: AssessmentReport, location: str) -> None:
        for field in fields:
            name = field.properties.get("InternalName", "")
            schema = field.properties.get("SchemaXml", "")
            loc = f"{location}/{name}"

            if 'ReadOnly="TRUE"' in schema:
                self.flag(
                    report,
                    "warning",
                    loc,
                    "ReadOnly field — cannot be written to via REST API",
                    "Strip ReadOnly attribute from SchemaXml before migrating",
                )

            if name in self.options.approval_workflow_fields:
                self.flag(
                    report,
                    "blocker",
                    loc,
                    f"{name} is a system approval workflow field — cannot be migrated",
                    "Enable EnableModeration=True on destination list to recreate natively",
                )

            dirty = [attr for attr in self.options.strip_field_attrs if f'{attr}="' in schema]
            if dirty:
                self.flag(
                    report,
                    "warning",
                    loc,
                    f"Schema contains internal attrs that must be stripped: {dirty}",
                    f"Strip before migrating: {sorted(self.options.strip_field_attrs)}",
                )
