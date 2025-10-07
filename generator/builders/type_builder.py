import ast
import importlib
import inspect
import os
import pkgutil
from functools import lru_cache
from os.path import abspath
from typing import Dict, List

from typing_extensions import Self

from generator.builders.member_builder import MemberBuilder
from generator.builders.property_builder import PropertyBuilder
from generator.builders.template_context import TemplateContext
from generator.documentation.baseservice import BaseDocumentationService
from office365.runtime.odata.type import ODataType
from office365.runtime.odata.type_information import TypeInformation


class TypeBuilder(ast.NodeTransformer):
    """Type builder"""

    def __init__(
        self,
        type_schema: TypeInformation,
        options: Dict[str, str] = None,
        docs_service: BaseDocumentationService = None,
    ):
        self._template = None
        self._schema = type_schema
        self._options = options
        self._type_info = None
        self._source_tree = None
        self._status = None
        self._properties = []
        self._members = []
        self._changes = []
        self._docstring = None
        self._entity_type_name_exists = False
        self._docs_service = docs_service

    def visit_ClassDef(self, node: ast.ClassDef):

        if self._schema:
            node.name = self.client_type_name

        [
            self._properties.append(PropertyBuilder(prop_schema))
            for _, prop_schema in self._schema.Properties.items()
        ]

        [
            self._members.append(MemberBuilder(member_schema))
            for _, member_schema in self._schema.Members.items()
        ]

        if self._docs_service:
            self._docs_service.build_documentation(self)

        self.generic_visit(node)

        if self._schema.BaseTypeFullName == "ComplexType":
            self._build_properties(node)
        elif self._schema.BaseTypeFullName == "EnumType":
            self._build_members(node)
        else:
            self._build_navigation_properties(node)

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
            # Track entity_type_name property
            if node.name == "entity_type_name":
                self._entity_type_name_exists = True

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
        self._template = TemplateContext(
            self._options.get("templatepath"), self._schema
        )

        if self.state == "attached":
            with open(self.file, encoding="utf-8") as f:
                self._source_tree = ast.parse(f.read())
            self._status = "updated"
        else:
            self._source_tree = self._template.load()
            self._status = "created"
        self.visit(self._source_tree)

        if self._status == "updated" and len(self._changes) == 0:
            self._status = None
        return self

    def _build_members(self, class_node: ast.ClassDef):
        if not self._members:
            return

        existing_members = self._get_existing_members(class_node)

        # Add missing members
        for member_builder in self._members:
            if member_builder.name not in existing_members:
                member_nodes = member_builder.build(self._template)
                class_node.body.extend(member_nodes)
                self._changes.append(f"member: {member_builder.name}")
                existing_members.add(member_builder.name)

    def _get_existing_members(self, class_node: ast.ClassDef) -> set:
        """Get set of existing member names in the class"""
        existing_members = set()

        for node in class_node.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        existing_members.add(target.id)
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                existing_members.add(node.target.id)

        return existing_members

    def _build_properties(self, class_node: ast.ClassDef):
        if not self._properties:
            return

        init_method = None

        for _, node in enumerate(class_node.body):
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
            args.append(prop.build_param())
            defaults.append(prop.build_default_value())

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
            body.append(prop.build_assign())
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
                init_method.args.args.append(prop.build_param())
                init_method.args.defaults.append(prop.build_default_value())
                init_method.body.append(prop.build_assign())
                self._changes.append(f"__init__ param: {prop.name}")

    def _build_navigation_properties(self, class_node: ast.ClassDef):
        """Build missing properties"""
        for prop in self._properties:
            if prop.status == "detached":
                property_methods = prop.build(self._template)

                for method in property_methods:
                    class_node.body.append(method)

    def _build_post(self, class_node: ast.ClassDef):
        """Remove pass statements if there are other statements in the class body"""
        if len(self._properties) == 0 and len(self._members) == 0:
            return

        class_node.body = [
            stmt for stmt in class_node.body if not isinstance(stmt, ast.Pass)
        ]

        self._ensure_entity_type_name(class_node)

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
                for _, name, _ in pkgutil.walk_packages(
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

    def _ensure_entity_type_name(self, class_node: ast.ClassDef):
        """Ensure the class has an entity_type_name property that returns the correct type name"""

        if self._schema.BaseTypeFullName not in [
            "ComplexType",
            "EntityType",
            "EnumType",
        ]:
            return

        parts = self._schema.FullName.split(".")
        if len(parts) <= 2:
            return

        if not self._entity_type_name_exists:
            entity_type_name_method = self._template.build_entity_type_name()
            class_node.body.append(entity_type_name_method)
            self._changes.append("entity_type_name property")

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

    @property
    def properties(self) -> List[PropertyBuilder]:
        return self._properties

    @property
    def members(self) -> List[MemberBuilder]:
        return self._members

    @property
    def entity_type_name(self) -> str:
        return self._schema.FullName
