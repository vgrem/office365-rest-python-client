import ast
from typing import List

from generator.builders.template_context import TemplateContext
from office365.runtime.odata.property import ODataProperty


class PropertyBuilder:

    def __init__(self, prop_schema: ODataProperty):
        self.prop_schema = prop_schema

    def build(self, template: TemplateContext) -> List[ast.stmt]:
        methods = [template.build_getter(self.prop_schema)]

        # setter = self.build_setter(self.prop_schema)
        # if setter is not None:
        #    methods.append(setter)

        return methods
