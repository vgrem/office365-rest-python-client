from __future__ import annotations

import ast
import builtins
import keyword
import re
from _ast import Assign, Call, Constant
from typing import TYPE_CHECKING, List, Optional

from office365.runtime.odata.type import ODataType

if TYPE_CHECKING:
    from generator.builders.template_context import TemplateContext
    from office365.runtime.odata.property import PropertyInformation


class PropertyBuilder:

    def __init__(self, schema: PropertyInformation, status="detached"):
        self.schema = schema
        self.status = status
        self.docstring: Optional[str] = None
        self._client_type: ODataType = ODataType(self.schema.TypeName, self.schema.IsNavigation)

    def build(self, template: TemplateContext) -> List[ast.stmt]:

        getter_node = template.build_get_property(self)

        # Add docstring if available
        if self.docstring and getter_node.body:
            docstring_node = ast.Expr(value=ast.Constant(value=self.docstring))
            getter_node.body.insert(0, docstring_node)

        # setter = self.build_set_property(self)

        return [getter_node]

    def build_param(self):
        """Build an ast.arg parameter"""
        return ast.arg(
            arg=self.name,
            annotation=(ast.Name(id=self.client_type_name, ctx=ast.Load()) if self.client_type_name else None),
        )

    def build_default_value(self) -> Constant | Call:
        """Build default value"""
        if self._client_type.is_primitive_type:
            return ast.Constant(value=None)
        else:
            return ast.Call(
                func=ast.Name(id=self.client_type_name, ctx=ast.Load()),
                args=[],
                keywords=[],
            )

    def build_assign(self) -> Assign:
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
    def client_type_name(self) -> str:
        return str(self._client_type)

    @property
    def client_item_type_name(self) -> str:
        return str(self._client_type.item_client_type)

    @property
    def is_collection_type(self) -> bool:
        return self._client_type.is_collection

    @property
    def is_object_type(self) -> bool:
        return self.schema.IsNavigation
