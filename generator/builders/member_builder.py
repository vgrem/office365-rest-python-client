import ast

from generator.builders.template_context import TemplateContext
from office365.runtime.odata.member import MemberInformation


class MemberBuilder:

    def __init__(self, schema: MemberInformation, status="detached"):
        self.schema = schema
        self.status = status

    def build(self, template: TemplateContext) -> list:
        """Build AST nodes for this member"""
        if self.status == "attached":
            return []

        member_assign = ast.Assign(
            targets=[ast.Name(id=self.name, ctx=ast.Store())],
            value=ast.Constant(value=self.value),
        )
        return [member_assign]

    @property
    def name(self):
        return self.schema.Name

    @property
    def value(self):
        return self.schema.Value
