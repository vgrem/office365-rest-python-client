from __future__ import annotations

import ast
import builtins
import keyword
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
        snake_case = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

        if keyword.iskeyword(snake_case) or hasattr(builtins, snake_case):
            return snake_case + "_"
        return snake_case

    @property
    def type_name(self) -> str:
        from office365.runtime.odata.type import ODataType

        model_type = ODataType.get_model_type(self.schema.type_name)
        if model_type:
            return model_type.__name__

        return self.schema.type_name

    @property
    def local_name(self) -> str:
        return self.type_name.rsplit('.', 1)[-1]
