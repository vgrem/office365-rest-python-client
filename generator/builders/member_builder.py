from __future__ import annotations

import ast
from typing import TYPE_CHECKING

from office365.runtime.odata.member import MemberInformation

if TYPE_CHECKING:
    from generator.builders.template_context import TemplateContext


class MemberBuilder:

    def __init__(self, schema: MemberInformation, status="detached"):
        self.schema = schema
        self.status = status
        self.docstring = None

    def build(self, template: TemplateContext) -> list:
        """Build AST nodes for this member"""
        if self.status == "attached":
            return []

        member_node = template.build_member(self)

        # Add docstring if available
        if self.docstring:
            # Create a docstring node before the assignment
            docstring_node = ast.Expr(value=ast.Constant(value=self.docstring))
            return [docstring_node, member_node]

        return [member_node]

    @property
    def name(self):
        if self.schema.Name in ["import", "None", "or", "and"]:
            return f"{self.schema.Name}_"
        return self.schema.Name

    @property
    def value(self):
        return self.schema.Value
