from __future__ import annotations

import ast
import datetime
import uuid
from typing import TYPE_CHECKING, List, Optional

from generator.builders import type_mapping
from generator.builders.naming import to_snake_case

if TYPE_CHECKING:
    from office365.runtime.odata.method import MethodInformation

_PRIMITIVE_DEFAULTS = {
    bool: "bool()",
    int: "int()",
    float: "float()",
    str: "str()",
    bytes: "b''",
    uuid.UUID: "uuid.UUID(int=0)",
    datetime.datetime: "datetime.min",
    datetime.date: "datetime.min",
    datetime.time: "datetime.min",
    datetime.timedelta: "datetime.timedelta(0)",
    dict: "{}",
}


def _primitive_default(type_name: str | None) -> str:
    """Default expression for a primitive OData type (e.g. ``Edm.Int32`` -> ``int()``)."""
    return _PRIMITIVE_DEFAULTS.get(type_mapping.primitive_type_for(type_name), "None")


class MethodBuilder:
    """Builds a Python method for an OData function/action.

    Bound operations become instance methods on the binding entity; unbound
    (type-encoded v3) operations become ``@staticmethod`` helpers that accept a
    client context.
    """

    def __init__(self, schema: MethodInformation, status: str = "detached"):
        self.schema = schema
        self.status = status
        self.docstring: Optional[str] = None
        self._return_type_name = schema.ReturnTypeFullName

    def build(self, context_type: str = "ClientContext") -> List[ast.stmt]:
        code = self.build_source(context_type)
        return list(ast.parse(code).body)

    def build_source(self, context_type: str = "ClientContext") -> str:
        schema = self.schema
        name = self.name
        params = [p for p in (schema.Parameters or []) if p.get("Name") not in (None, "this", "bindingParameter")]
        args = ", ".join(f"{self._param_name(p)}: {self._param_type(p)}" for p in params)
        payload = ", ".join(f'"{p["Name"]}": {self._param_name(p)}' for p in params)
        method_params = ", ".join(self._param_name(p) for p in params)

        docstring = self._build_docstring(params)
        if schema.IsStatic:
            binding_type = type_mapping.client_type_name(schema.BindingTypeFullName)
            signature = f"{name}(context" + (f", {args}" if args else "") + f") -> {self.return_annotation('context')}"
            if schema.Kind == "function":
                body = (
                    f"return_type = {self._return_default(context_type)}\n"
                    f'qry = FunctionQuery({binding_type}(context), "{schema.Name}", [{method_params}], return_type)\n'
                    f"context.add_query(qry)\n"
                    f"return return_type"
                )
            else:
                body = (
                    f"return_type = {self._return_default(context_type)}\n"
                    f"qry = ServiceOperationQuery(\n"
                    f'    {binding_type}(context), "{schema.Name}", None, {{{payload}}}, None, return_type, True\n'
                    f")\n"
                    f"context.add_query(qry)\n"
                    f"return return_type"
                )
            return f"@staticmethod\ndef {signature}:\n{self._indent(docstring)}\n{self._indent(body)}\n"

        signature = f"{name}(self" + (f", {args}" if args else "") + f") -> {self.return_annotation('self.context')}"
        if not schema.ReturnTypeFullName:
            body = f'qry = ServiceOperationQuery(self, "{schema.Name}")\nself.context.add_query(qry)\nreturn self'
        elif schema.Kind == "function":
            body = (
                f"return_type = {self._return_default('self.context')}\n"
                f'qry = FunctionQuery(self, "{schema.Name}", [{method_params}], return_type)\n'
                f"self.context.add_query(qry)\n"
                f"return return_type"
            )
        else:
            body = (
                f"return_type = {self._return_default('self.context')}\n"
                f'qry = ServiceOperationQuery(self, "{schema.Name}", None, {{{payload}}}, None, return_type)\n'
                f"self.context.add_query(qry)\n"
                f"return return_type"
            )
        return f"def {signature}:\n{self._indent(docstring)}\n{self._indent(body)}\n"

    @staticmethod
    def _indent(text: str, spaces: int = 4) -> str:
        prefix = " " * spaces
        return "\n".join(prefix + line if line else line for line in text.splitlines())

    def _return_default(self, context: str) -> str:
        return_type = self.schema.ReturnTypeFullName
        if return_type is None:
            return "None"
        if self.is_collection:
            item_type = return_type[len("Collection(") : -1]
            collection_defaults = {"Edm.String": "StringCollection()", "Edm.Guid": "GuidCollection()"}
            default = collection_defaults.get(item_type)
            if default is None:
                primitive = type_mapping.primitive_type_for(item_type)
                default = (
                    f"ClientValueCollection({primitive.__name__})"
                    if primitive is not None
                    else f"{self.client_type_name}()"
                )
            return f"ClientResult({context}, {default})"
        if self.is_primitive:
            return f"ClientResult({context}, {_primitive_default(return_type)})"
        return f"{self.client_type_name}({context})"

    def _build_docstring(self, params: list) -> str:
        lines = [f'"""{self.schema.Name} operation.']
        if params:
            lines.append("")
            lines.append("Args:")
            for param in params:
                lines.append(f"    {self._param_name(param)} ({self._param_type(param)}): {param.get('Name')} parameter")
        lines.append('"""')
        return "\n    ".join(lines)

    def return_annotation(self, context: str) -> str:
        """The Python return annotation for the generated method."""
        if not self.schema.ReturnTypeFullName:
            return "None" if self.schema.IsStatic else "Self"
        if self.is_primitive or self.is_collection:
            return f"ClientResult[{self.client_type_name}]"
        return self.client_type_name

    @property
    def name(self) -> str:
        return to_snake_case(self.schema.Name or "")

    @property
    def client_type_name(self) -> str:
        return type_mapping.client_type_name(self._return_type_name)

    @property
    def is_primitive(self) -> bool:
        return type_mapping.is_primitive_name(self._return_type_name)

    @property
    def is_collection(self) -> bool:
        return type_mapping.is_collection(self._return_type_name)

    def _param_name(self, param: dict) -> str:
        return to_snake_case(param.get("Name") or "arg")

    def _param_type(self, param: dict) -> str:
        type_name = param.get("Type")
        if type_name is None:
            return "str"
        return type_mapping.client_type_name(type_name)
