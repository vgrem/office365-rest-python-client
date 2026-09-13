from __future__ import annotations

import ast
from typing import TYPE_CHECKING, List, Optional

from generator.builders import type_mapping
from generator.builders.naming import to_snake_case
from generator.builders.type_descriptor import ReturnType

if TYPE_CHECKING:
    from office365.runtime.odata.method import MethodInformation

    from generator.builders.type_resolver import ClientTypeResolver


class MethodBuilder:
    """Builds a Python method for an OData function/action.

    Bound operations become instance methods on the binding entity; unbound
    (type-encoded v3) operations become ``@staticmethod`` helpers that accept a
    client context.
    """

    def __init__(
        self,
        schema: MethodInformation,
        status: str = "detached",
        resolver: Optional["ClientTypeResolver"] = None,
    ):
        self.schema = schema
        self.status = status
        self.docstring: Optional[str] = None
        self._return_type = ReturnType(schema.ReturnTypeFullName, resolver)

    def build(self, context_type: str = "ClientContext") -> List[ast.stmt]:
        return list(ast.parse(self.build_source(context_type)).body)

    def build_source(self, context_type: str = "ClientContext") -> str:
        schema = self.schema
        params = self._params()
        is_static = bool(schema.IsStatic)
        receiver = f"{type_mapping.client_type_name(schema.BindingTypeFullName)}(context)" if is_static else "self"
        context_expr = "context" if is_static else "self.context"
        signature = self._signature(context_type, params, is_static)
        body = self._body(receiver, context_expr, params, is_static)
        prefix = "@staticmethod\n" if is_static else ""
        return f"{prefix}def {signature}:\n{self._indent(self._docstring(params))}\n{self._indent(body)}\n"

    def _signature(self, context_type: str, params: list, is_static: bool) -> str:
        first = f"context: {context_type}" if is_static else "self"
        args = "".join(f", {self._param_name(p)}: {self._param_type(p)}" for p in params)
        return f"{self.name}({first}{args}) -> {self.return_annotation}"

    def _body(self, receiver: str, context_expr: str, params: list, is_static: bool) -> str:
        if self._return_type.is_void:
            query = self._query(receiver, params, is_static, "None")
            result = "None" if is_static else "self"
            return f"qry = {query}\n{context_expr}.add_query(qry)\nreturn {result}"
        default = self._return_type.default(context_expr)
        query = self._query(receiver, params, is_static, "return_type")
        return f"return_type = {default}\nqry = {query}\n{context_expr}.add_query(qry)\nreturn return_type"

    def _query(self, receiver: str, params: list, is_static: bool, return_type: str) -> str:
        schema = self.schema
        method_params = ", ".join(self._param_name(p) for p in params)
        if schema.Kind == "function":
            raw_content = ", return_raw_content=True" if self._return_type.is_stream else ""
            return f'FunctionQuery({receiver}, "{schema.Name}", [{method_params}], {return_type}{raw_content})'
        payload = ", ".join(f'"{p["Name"]}": {self._param_name(p)}' for p in params)
        static = ", True" if is_static else ""
        return f'ServiceOperationQuery({receiver}, "{schema.Name}", None, {{{payload}}}, None, {return_type}{static})'

    @staticmethod
    def _indent(text: str, spaces: int = 4) -> str:
        prefix = " " * spaces
        return "\n".join(prefix + line if line else line for line in text.splitlines())

    def _params(self) -> list:
        return [p for p in (self.schema.Parameters or []) if p.get("Name") not in (None, "this", "bindingParameter")]

    def _docstring(self, params: list) -> str:
        lines = [f'"""{self.schema.Name} operation.']
        if params:
            lines.append("")
            lines.append("Args:")
            for param in params:
                lines.append(f"    {self._param_name(param)} ({self._param_type(param)}): {param.get('Name')} parameter")
        lines.append('"""')
        return "\n    ".join(lines)

    @property
    def return_annotation(self) -> str:
        """The Python return annotation for the generated method."""
        if self._return_type.is_void:
            return "None" if self.schema.IsStatic else "Self"
        return self._return_type.annotation

    @property
    def name(self) -> str:
        return to_snake_case(self.schema.Name or "")

    def _param_name(self, param: dict) -> str:
        return to_snake_case(param.get("Name") or "arg")

    def _param_type(self, param: dict) -> str:
        type_name = param.get("Type")
        if type_name is None:
            return "str"
        return type_mapping.client_type_name(type_name)
