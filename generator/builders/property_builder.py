from __future__ import annotations

import ast
import re
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
   from generator.builders.template_context import TemplateContext
   from office365.runtime.odata.property import ODataProperty


class PropertyBuilder:

    def __init__(self, prop_schema: ODataProperty):
        self.schema = prop_schema

    def build(self, template: TemplateContext) -> List[ast.stmt]:
        methods = [template.build_getter(self)]

        # setter = self.build_setter(self)
        # if setter is not None:
        #    methods.append(setter)

        return methods

    @property
    def name(self) -> str:
        """Convert CamelCase to snake_case"""
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", self.schema.name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    @property
    def type_name(self) -> str:
        from office365.runtime.odata.type import ODataType

        if self.schema.type_name in ODataType.primitive_types.values():
            python_type = next(
                (
                    key
                    for key, value in ODataType.primitive_types.items()
                    if value == self.schema.type_name
                ),
                None,
            )
            if python_type:
                return python_type.__name__
        return self.schema.type_name
