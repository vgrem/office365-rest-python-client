from __future__ import annotations

import ast
import builtins
import keyword
import re
from typing import TYPE_CHECKING, List

from office365.runtime.odata.type import ODataType

if TYPE_CHECKING:
    from generator.builders.template_context import TemplateContext
    from office365.runtime.odata.property import PropertyInformation


class PropertyBuilder:

    def __init__(self, schema: PropertyInformation, status="detached"):
        self.schema = schema
        self.status = status

    def build(self, template: TemplateContext) -> List[ast.stmt]:
        methods = [template.build_getter(self)]

        # setter = self.build_setter(self)
        # if setter is not None:
        #    methods.append(setter)

        return methods

    def build_param(self):
        """Build an ast.arg parameter"""
        return ast.arg(
            arg=self.name,
            annotation=(
                ast.Name(id=self.client_type, ctx=ast.Load())
                if self.type_name
                else None
            ),
        )

    def build_default(self):
        """Build default value"""
        if ODataType.is_primitive_type(self.schema.TypeName):
            return ast.Constant(value=None)
        else:
            return ast.Call(
                func=ast.Name(id=self.client_type, ctx=ast.Load()),
                args=[],
                keywords=[],
            )

    def build_assign(self):
        """Build assignment statement"""
        return ast.Assign(
            targets=[
                ast.Attribute(
                    value=ast.Name(id="self", ctx=ast.Load()),
                    attr=self.schema.Name,
                    ctx=ast.Store(),
                )
            ],
            value=ast.Name(id=self.name, ctx=ast.Load()),
        )

    @property
    def name(self) -> str:
        """Convert CamelCase to snake_case"""
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", self.schema.Name)
        snake_case = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

        if keyword.iskeyword(snake_case) or hasattr(builtins, snake_case):
            return snake_case + "_"
        return snake_case

    @property
    def type_name(self) -> str:
        from office365.runtime.odata.type import ODataType

        model_type = ODataType.get_client_type(self.schema.TypeName)
        if model_type:
            return model_type.__name__

        return self.schema.TypeName

    @property
    def client_type(self) -> str:
        return ODataType.resolve_client_type(self.type_name)
