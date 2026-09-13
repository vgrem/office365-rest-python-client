from __future__ import annotations

import ast
from _ast import Assign, Call, Constant
from typing import TYPE_CHECKING, List, Optional

from office365.runtime.odata.type import ODataType

from generator.builders import type_mapping
from generator.builders.naming import to_snake_case

if TYPE_CHECKING:
    from generator.builders.template_context import TemplateContext
    from generator.builders.type_resolver import ClientTypeResolver
    from generator.odata.property import PropertyInformation


class PropertyBuilder:
    def __init__(self, schema: PropertyInformation, status="detached", resolver: Optional["ClientTypeResolver"] = None):
        self.schema = schema
        self.status = status
        self.docstring: Optional[str] = None
        self._resolver = resolver

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
        if self.is_collection_type:
            base_name = self.client_type_name.split("[")[0]
            if ODataType.is_primitive_name(self.schema.TypeName):
                return ast.Call(
                    func=ast.Name(id="field", ctx=ast.Load()),
                    args=[],
                    keywords=[
                        ast.keyword(
                            arg="default_factory",
                            value=ast.Name(id=base_name, ctx=ast.Load()),
                        )
                    ],
                )
            else:
                item_name = self.client_item_type_name
                return ast.Call(
                    func=ast.Name(id="field", ctx=ast.Load()),
                    args=[],
                    keywords=[
                        ast.keyword(
                            arg="default_factory",
                            value=ast.Lambda(
                                args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]),
                                body=ast.Call(
                                    func=ast.Name(id=base_name, ctx=ast.Load()),
                                    args=[ast.Name(id=item_name, ctx=ast.Load())],
                                    keywords=[],
                                ),
                            ),
                        )
                    ],
                )
        elif ODataType.is_primitive_name(self.schema.TypeName):
            if self.client_type_name == "datetime":
                return ast.Call(
                    func=ast.Name(id="field", ctx=ast.Load()),
                    args=[],
                    keywords=[
                        ast.keyword(
                            arg="default_factory",
                            value=ast.Lambda(
                                args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]),
                                body=ast.Attribute(
                                    value=ast.Name(id="datetime", ctx=ast.Load()),
                                    attr="min",
                                    ctx=ast.Load(),
                                ),
                            ),
                        )
                    ],
                )
            return ast.Constant(value=None)
        else:
            return ast.Call(
                func=ast.Name(id="field", ctx=ast.Load()),
                args=[],
                keywords=[
                    ast.keyword(
                        arg="default_factory",
                        value=ast.Name(id=self.client_type_name, ctx=ast.Load()),
                    )
                ],
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

    def resolve_client_type(self):
        """Resolves the property's OData type to its generated Python class."""
        return self._resolver.resolve(self.schema.TypeName) if self._resolver is not None else None

    @property
    def name(self) -> str:
        """Convert CamelCase to snake_case"""
        return to_snake_case(self.schema.Name)

    @property
    def client_type_name(self) -> str:
        return type_mapping.client_type_name(self.schema.TypeName, self.is_object_type)

    @property
    def client_item_type_name(self) -> str:
        return type_mapping.item_client_type_name(self.schema.TypeName, self.is_object_type)

    @property
    def is_collection_type(self) -> bool:
        return ODataType.is_collection_name(self.schema.TypeName)

    @property
    def is_object_type(self) -> bool:
        return self.schema.IsNavigation or False
