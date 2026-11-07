from __future__ import annotations

import ast
from typing import TYPE_CHECKING, List, Optional

from generator.build.naming import item_name, python_name, to_snake_case
from generator.model_index.references import ParameterType, ReturnType, TypeKind
from generator.odata.type_system import TypeRef

#: Max length of a docstring ``Args`` line's head, including the re-indentation
#: applied after ``_docstring`` returns (ruff does not reflow docstring prose).
_MAX_DOCSTRING_ARG = 105

if TYPE_CHECKING:
    from generator.model_index.resolution import TypeRegistry
    from generator.odata.method import MethodInformation


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
        resolver: Optional["TypeRegistry"] = None,
        client_value_types: frozenset[str] = frozenset(),
        named_parameters: bool = False,
    ):
        self.schema = schema
        self.status = status
        self.docstring: Optional[str] = None
        self._resolver = resolver
        self._named_parameters = named_parameters
        self._return_type = ReturnType(schema.ReturnTypeFullName, resolver, client_value_types)

    def build(self, context_type: str = "ClientContext") -> List[ast.stmt]:
        return list(ast.parse(self.build_source(context_type)).body)

    def build_source(self, context_type: str = "ClientContext") -> str:
        schema = self.schema
        params = self._params()
        is_static = bool(schema.IsStatic)
        receiver = f"{python_name(schema.BindingTypeFullName)}(context)" if is_static else "self"
        context_expr = "context" if is_static else "self.context"
        signature = self._signature(context_type, params, is_static)
        body = self._body(receiver, context_expr, params, is_static)
        imports = self.runtime_imports()
        if imports:
            body = "\n".join(imports) + "\n" + body
        prefix = "@staticmethod\n" if is_static else ""
        return f"{prefix}def {signature}:\n{self._indent(self._docstring(params))}\n{self._indent(body)}\n"

    def runtime_imports(self) -> List[str]:
        """Local imports for types the method constructs at runtime (cycle-safe).

        The module is resolved from the OData name, never from the class name alone: two
        namespaces may declare the same class name (``microsoft.graph.Operation`` and
        ``microsoft.graph.partners.billing.operation``), and a bare-name lookup picks
        whichever the index lists first.
        """
        if self._resolver is None:
            return []
        imports = []
        for type_name in self._runtime_type_names():
            module = self._resolver.module_for(type_name)
            if module:
                imports.append(f"from {module} import {item_name(type_name)}")
        return sorted(set(imports))

    def _runtime_type_names(self) -> List[str]:
        """OData names of the types referenced inside the method body."""
        schema = self.schema
        names: List[str] = []
        if schema.IsStatic and schema.BindingTypeFullName:
            names.append(schema.BindingTypeFullName)
        non_scalar = (
            TypeKind.ENTITY,
            TypeKind.ENTITY_COLLECTION,
            TypeKind.CLIENT_VALUE,
            TypeKind.CLIENT_VALUE_COLLECTION,
        )
        if schema.ReturnTypeFullName and self._return_type.kind in non_scalar:
            names.append(schema.ReturnTypeFullName)
        return [TypeRef.parse(name).name or "" for name in names if name]

    def _signature(self, context_type: str, params: list, is_static: bool) -> str:
        first = f"context: {context_type}" if is_static else "self"
        args = "".join(f", {self._param_name(p)}: {self._param_type(p)}" for p in params)
        return f"{self.name}({first}{args}) -> {self.return_annotation}"

    def _body(self, receiver: str, context_expr: str, params: list, is_static: bool) -> str:
        if self._return_type.is_void:
            query = self._query(receiver, params, is_static, "None")
            body = f"qry = {query}\n{context_expr}.add_query(qry)"
            return body if is_static else f"{body}\nreturn self"
        local = self._result_local(params)
        default = self._return_type.default(context_expr)
        query = self._query(receiver, params, is_static, local)
        return f"{local} = {default}\nqry = {query}\n{context_expr}.add_query(qry)\nreturn {local}"

    def _result_local(self, params: list) -> str:
        """The local that holds the returned object, named so no parameter shadows it.

        An operation may declare a parameter called ``returnType`` (the workbook
        functions do); naming the local after it would send the returned object where
        the caller's own value belongs.
        """
        taken = {self._param_name(param) for param in params}
        name = "return_type"
        while name in taken:
            name += "_"
        return name

    def _query(self, receiver: str, params: list, is_static: bool, return_type: str) -> str:
        schema = self.schema
        if schema.Kind == "function":
            raw_content = ", return_raw_content=True" if self._return_type.is_stream else ""
            arguments = self._call_parameters(params)
            return f'FunctionQuery({receiver}, "{schema.Name}", {arguments}, {return_type}{raw_content})'
        payload = ", ".join(f'"{p["Name"]}": {self._param_value(p)}' for p in params)
        static = ", True" if is_static else ""
        return f'ServiceOperationQuery({receiver}, "{schema.Name}", None, {{{payload}}}, None, {return_type}{static})'

    def _call_parameters(self, params: list) -> str:
        """The parameters of a function call, in the spelling the service matches by.

        Graph matches a function's parameters by name (``reminderView(startDateTime=...)``)
        and rejects an unnamed list as an unknown navigation property; OData v3
        operations are addressed positionally.
        """
        if not params:
            return "None"
        if self._named_parameters:
            named = ", ".join(f'"{p["Name"]}": {self._param_value(p)}' for p in params)
            return f"{{{named}}}"
        return "[" + ", ".join(self._param_value(p) for p in params) + "]"

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
                # Keep each line short: the docstring is re-indented before emission,
                # and ruff does not reflow docstring prose (see E501).
                head = f"    {self._param_name(param)} ({self._param_type(param)}):"
                lines.append(head if len(head) <= _MAX_DOCSTRING_ARG else f"    {self._param_name(param)}:")
                lines.append(f"        {param.get('Name')} parameter")
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
        return to_snake_case(self.schema.Name or "", avoid_builtins=False)

    def _param_name(self, param: dict) -> str:
        return to_snake_case(param.get("Name") or "arg", avoid_builtins=True)

    def _param_type(self, param: dict) -> str:
        type_name = param.get("Type")
        if type_name is None:
            return "str"
        return ParameterType(str(type_name)).annotation

    def _param_value(self, param: dict) -> str:
        type_name = param.get("Type")
        name = self._param_name(param)
        if type_name is None:
            return name
        return ParameterType(str(type_name)).wrap(name)
