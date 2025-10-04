import ast
import importlib
import inspect
import os
import pkgutil
from functools import lru_cache
from os.path import abspath
from typing import Dict

from typing_extensions import Self

from generator.builders.property_builder import PropertyBuilder
from generator.builders.template_context import TemplateContext
from office365.runtime.odata.type import ODataType
from office365.runtime.odata.type_information import TypeInformation


class TypeBuilder(ast.NodeTransformer):
    """Type builder"""

    def __init__(self, type_schema: TypeInformation, options: Dict[str, str] = None):
        self._template = None
        self._schema = type_schema
        self._options = options
        self._type_info = None
        self._source_tree = None
        self._status = None
        self._properties = []
        self._changes = []

    def visit_ClassDef(self, node: ast.ClassDef):
        if self._schema:
            node.name = self.client_type_name

        if self._schema and self._schema.Properties:
            for prop_name, prop_schema in self._schema.Properties.items():
                builder = PropertyBuilder(prop_schema)
                builder.status = "detached"
                self._properties.append(builder)

        self.generic_visit(node)

        if self._schema.BaseTypeFullName == "ComplexType":
            self._build_properties(node)
        else:
            self._build_nav_properties(node)

        self._build_post(node)

        return node

    def visit_FunctionDef(self, node):

        if node.name == "__init__":
            return self.generic_visit(node)

        is_property = False
        for decorator in node.decorator_list:
            if (isinstance(decorator, ast.Name) and decorator.id == "property") or (
                isinstance(decorator, ast.Attribute) and decorator.attr == "property"
            ):
                is_property = True
                break

        if is_property:
            matching_prop = next(
                (prop for prop in self._properties if prop.name == node.name), None
            )
            if matching_prop:
                matching_prop.status = "attached"

        return self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        if (
            isinstance(node.ctx, ast.Store)
            and isinstance(node.value, ast.Name)
            and node.value.id == "self"
            and isinstance(node.attr, str)
        ):

            prop_name = node.attr
            matching_prop = next(
                (prop for prop in self._properties if prop.name == prop_name), None
            )
            if matching_prop:
                matching_prop.status = "attached"

        return node

    def build(self) -> Self:
        self._template = TemplateContext(self._options.get("templatepath"))
        if self.state == "attached":
            with open(self.file, encoding="utf-8") as f:
                self._source_tree = ast.parse(f.read())
            self._status = "updated"
        else:
            self._source_tree = self._template.load(self._schema)
            self._status = "created"
        self.visit(self._source_tree)

        if self._status == "updated" and len(self._changes) == 0:
            self._status = None
        return self

    def _build_properties(self, class_node: ast.ClassDef):
        if not self._properties:
            return

        init_method = None

        for i, node in enumerate(class_node.body):
            if isinstance(node, ast.FunctionDef) and node.name == "__init__":
                init_method = node
                break

        if init_method is None:
            init_method = self._build_init_method()
            class_node.body.insert(0, init_method)
        else:
            self._update_init_method(init_method)

    def _build_init_method(self) -> ast.FunctionDef:
        args = [ast.arg(arg="self", annotation=None)]
        defaults = []

        for prop in self._properties:
            param = ast.arg(
                arg=prop.name,
                annotation=(
                    ast.Name(id=prop.client_type, ctx=ast.Load())
                    if prop.type_name
                    else None
                ),
            )
            args.append(param)
            if ODataType.is_primitive_type(prop.schema.TypeName):
                defaults.append(ast.Constant(value=None))
            else:
                defaults.append(
                    ast.Call(
                        func=ast.Name(id=prop.client_type, ctx=ast.Load()),
                        args=[],
                        keywords=[],
                    )
                )

        function_args = ast.arguments(
            posonlyargs=[],
            args=args,
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=defaults,
        )

        body = []
        for prop in self._properties:
            assign = ast.Assign(
                targets=[
                    ast.Attribute(
                        value=ast.Name(id="self", ctx=ast.Load()),
                        attr=prop.schema.Name,
                        ctx=ast.Store(),
                    )
                ],
                value=ast.Name(id=prop.name, ctx=ast.Load()),
            )
            body.append(assign)
            self._changes.append(f"__init__ param: {prop.name}")

        init_method = ast.FunctionDef(
            name="__init__",
            args=function_args,
            body=body,
            decorator_list=[],
            returns=None,
        )
        return init_method

    def _update_init_method(self, init_method: ast.FunctionDef):

        existing_params = {
            arg.arg for arg in init_method.args.args if arg.arg != "self"
        }

        for prop in self._properties:
            if prop.name not in existing_params and prop.status == "detached":
                param = ast.arg(
                    arg=prop.name,
                    annotation=(
                        ast.Name(id=prop.type_name, ctx=ast.Load())
                        if prop.type_name
                        else None
                    ),
                )
                init_method.args.args.append(param)
                init_method.args.defaults.append(ast.Constant(value=None))

                assign = ast.Assign(
                    targets=[
                        ast.Attribute(
                            value=ast.Name(id="self", ctx=ast.Load()),
                            attr=prop.schema.Name,
                            ctx=ast.Store(),
                        )
                    ],
                    value=ast.Name(id=prop.Name, ctx=ast.Load()),
                )
                init_method.body.append(assign)
                self._changes.append(f"__init__ param: {prop.Name}")

    def _build_nav_properties(self, class_node: ast.ClassDef):
        """Build missing properties"""
        for prop in self._properties:
            if prop.status == "detached":
                property_methods = prop.build(self._template)

                for method in property_methods:
                    class_node.body.append(method)

    def _build_post(self, class_node: ast.ClassDef):
        """Remove pass statements if there are other statements in the class body"""
        if len(self._properties) == 0:
            return

        class_node.body = [
            stmt for stmt in class_node.body if not isinstance(stmt, ast.Pass)
        ]

    def save(self):
        ast.fix_missing_locations(self._source_tree)
        code = ast.unparse(self._source_tree)

        with open(self.file, "w", encoding="utf-8") as f:
            f.write(code)

    @lru_cache(maxsize=512)
    def _find_model_class(self, class_name: str):
        for module_name in self._options["modules"].split(","):
            try:
                module = importlib.import_module(module_name.strip())
                for _, name, is_pkg in pkgutil.walk_packages(
                    module.__path__, module.__name__ + "."
                ):
                    submodule = importlib.import_module(name)
                    if hasattr(submodule, class_name):
                        cls = getattr(submodule, class_name)
                        if inspect.isclass(cls):
                            return cls
            except (ImportError, AttributeError):
                continue
        return None

    def _resolve_type(self) -> Dict[str, str]:
        type_info = {}

        cls = self._find_model_class(self.client_type_name)
        if cls is not None:
            type_info["state"] = "attached"
            type_info["file"] = inspect.getsourcefile(cls)
        else:
            type_info["state"] = "detached"
            type_info["file"] = abspath(
                os.path.join(
                    self._options["outputpath"], self.client_type_name.lower() + ".py"
                )
            )
        return type_info

    def _ensure_type_info(self):
        if self._type_info is None:
            self._type_info = self._resolve_type()
        return self._type_info

    @property
    def state(self):
        self._ensure_type_info()
        return self._type_info["state"]

    @property
    def file(self):
        self._ensure_type_info()
        return self._type_info["file"]

    @property
    def status(self):
        return self._status

    @property
    def client_type_name(self):
        return ODataType.resolve_client_type(self._schema.FullName)
