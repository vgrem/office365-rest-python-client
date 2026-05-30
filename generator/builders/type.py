import ast
import inspect
import os
import re
from _ast import Module
from enum import Enum
from os.path import abspath
from typing import Dict, List, Optional

from office365.runtime.odata.type import ODataType
from office365.runtime.odata.type_information import TypeInformation
from typing_extensions import Self

from generator.builders.member import MemberBuilder
from generator.builders.property import PropertyBuilder
from generator.builders.template_context import TemplateContext
from generator.documentation.baseservice import BaseDocumentationService


class TypeBuilder(ast.NodeTransformer):
    """Type builder"""

    def __init__(
        self,
        type_schema: TypeInformation,
        options: Optional[Dict[str, str]] = None,
        docs_service: Optional[BaseDocumentationService] = None,
    ):
        self._schema = type_schema
        self._options = options
        self._docs_service = docs_service
        self._template: Optional[TemplateContext] = None
        self._type_info: Optional[Dict] = None
        self._source_tree: Optional[Module] = None
        self._status: Optional[str] = None
        self._properties: List[PropertyBuilder] = []
        self._members: List[MemberBuilder] = []
        self._changes: List[str] = []
        self._docstring: Optional[str] = None
        self._entity_type_name_exists: bool = False
        self._client_type: ODataType = ODataType(self._schema.FullName, self._schema.IsValueObject or False)

    def visit_ClassDef(self, node: ast.ClassDef):
        if self._schema:
            node.name = self.client_type_name

        options = self._options or {}
        [
            self._properties.append(PropertyBuilder(prop_schema))
            for name, prop_schema in self._schema.Properties.items()
            if name not in options.get("ignoredproperties", [])
        ]

        [self._members.append(MemberBuilder(member_schema)) for _, member_schema in self._schema.Members.items()]

        if self._docs_service:
            self._docs_service.build_documentation(self)

        self.generic_visit(node)

        if self._schema.BaseTypeFullName == "ComplexType":
            self._build_value_properties(node)
        elif self._schema.BaseTypeFullName == "EnumType":
            self._build_members(node)
        else:
            self._build_object_properties(node)

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

            matching_prop = next((prop for prop in self._properties if prop.name == node.name), None)
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
            matching_prop = next((prop for prop in self._properties if prop.name == prop_name), None)
            if matching_prop:
                matching_prop.status = "attached"

        return node

    def build(self) -> Self:
        assert self._options is not None
        self._template = TemplateContext(self._options.get("templatepath", ""), self._schema)

        if self.state == "attached":
            with open(self.file, encoding="utf-8") as f:
                self._source_tree = ast.parse(f.read())
            self._status = "updated"
        else:
            self._source_tree = self._template.load()
            self._status = "created"
        self.visit(self._source_tree)
        self._build_imports(self._source_tree)

        if self._status == "updated" and len(self._changes) == 0:
            self._status = None
        return self

    def _build_imports(self, module: ast.Module):
        """Build missing imports"""
        assert self._template is not None
        imports = self._template.build_imports(self)

        existing_imports = [n for n in module.body if isinstance(n, (ast.Import, ast.ImportFrom))]
        insert_index = len(existing_imports)
        for imp in imports:
            module.body.insert(insert_index, imp)
            insert_index += 1

    def _build_members(self, class_node: ast.ClassDef):
        if not self._members:
            return

        assert self._template is not None
        existing_members = self._template.get_existing_members(class_node)

        # Add missing members
        for member_builder in self._members:
            if member_builder.name not in existing_members:
                assert self._template is not None
                member_nodes = member_builder.build(self._template)
                class_node.body.extend(member_nodes)
                self._changes.append(f"member: {member_builder.name}")
                existing_members.add(member_builder.name)

    def _build_value_properties(self, class_node: ast.ClassDef):
        if not self._properties:
            return

        # Remove any existing __init__ (dataclass generates it)
        class_node.body = [n for n in class_node.body if not (isinstance(n, ast.FunctionDef) and n.name == "__init__")]

        existing_anns = {
            n.target.id if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) else None
            for n in class_node.body
        }

        for prop in self._properties:
            if prop.schema.Name in existing_anns:
                continue
            ann = self._build_value_annotation(prop)
            class_node.body.insert(len(class_node.body) - 1, ann)
            self._changes.append(f"property annotation: {prop.schema.Name}")

    def _build_value_annotation(self, prop: PropertyBuilder) -> ast.AnnAssign:
        """Build a class-level type annotation for a ClientValue property.

        Uses the original OData property name (e.g. taskScope) rather than
        the snake_case Python name, matching the JSON serialization contract.
        """
        prop_type = prop.client_type_name
        if prop_type in TemplateContext.OPTIONAL_TYPES:
            annotation = ast.BinOp(
                left=ast.Name(id=prop_type, ctx=ast.Load()),
                op=ast.BitOr(),
                right=ast.Constant(value=None),
            )
        else:
            annotation = ast.Name(id=prop_type, ctx=ast.Load())

        if prop.is_object_type:
            # Navigation properties on ClientValue can't be instantiated
            # without context — use None as safe default
            default = ast.Constant(value=None)
            if "Optional" not in str(annotation) and prop_type not in TemplateContext.OPTIONAL_TYPES:
                # Make annotation Optional so None is valid
                annotation = ast.BinOp(
                    left=ast.Name(id=prop_type, ctx=ast.Load()),
                    op=ast.BitOr(),
                    right=ast.Constant(value=None),
                )
        else:
            default = prop.build_default_value()

            # Resolve enum types to use first member as default instead of EnumType()
            if self._options and not prop.is_collection_type:
                modules = tuple(self._options.get("modules", "").split(","))
                resolved = prop._client_type.resolve_client_type(modules)
                if resolved is not None and inspect.isclass(resolved) and issubclass(resolved, Enum):
                    members = list(resolved)
                    if members:
                        default = ast.Attribute(
                            value=ast.Name(id=prop_type, ctx=ast.Load()),
                            attr=members[0].name,
                            ctx=ast.Load(),
                        )

        return ast.AnnAssign(
            target=ast.Name(id=prop.schema.Name, ctx=ast.Store()),
            annotation=annotation,
            value=default,
            simple=1,
        )

    def _build_object_properties(self, class_node: ast.ClassDef):
        """Build missing properties"""
        for prop in self._properties:
            if prop.status == "detached":
                assert self._template is not None
                property_methods = prop.build(self._template)

                for method in property_methods:
                    class_node.body.append(method)

    def _build_post(self, class_node: ast.ClassDef):
        """Remove pass statements if there are other statements in the class body"""
        if len(self._properties) == 0 and len(self._members) == 0:
            return

        class_node.body = [stmt for stmt in class_node.body if not isinstance(stmt, ast.Pass)]

        self._ensure_entity_type_name(class_node)

    def save(self):
        assert self._source_tree is not None
        ast.fix_missing_locations(self._source_tree)
        code = ast.unparse(self._source_tree)

        with open(self.file, "w", encoding="utf-8") as f:
            f.write(code)

    def _ensure_entity_type_name(self, class_node: ast.ClassDef):
        """Ensure the class has an entity_type_name property that returns the correct type name"""

        if self._schema.BaseTypeFullName not in [
            "ComplexType",
            "EntityType",
            "EnumType",
        ]:
            return

        parts = self._schema.FullName.split(".")
        MIN_NAME_PARTS = 2
        if len(parts) <= MIN_NAME_PARTS:
            return

        if not self._entity_type_name_exists:
            assert self._template is not None
            entity_type_name_method = self._template.build_type_name_property()
            class_node.body.append(entity_type_name_method)
            self._changes.append("entity_type_name property")

    @staticmethod
    def _to_snake_case(name: str) -> str:
        """Convert PascalCase or UpperCamelCase to snake_case."""
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    def _resolve_type(self) -> Dict[str, str]:
        type_info: Dict[str, str] = {}

        assert self._options is not None
        cls = self._client_type.resolve_client_type(tuple(self._options["modules"].split(",")))
        if cls is not None:
            type_info["state"] = "attached"
            type_info["file"] = inspect.getsourcefile(cls) or ""
        else:
            type_info["state"] = "detached"
            type_info["file"] = abspath(
                os.path.join(self._options["outputpath"], self._to_snake_case(self.client_type_name) + ".py")
            )
        return type_info

    def _ensure_type_info(self):
        if self._type_info is None:
            self._type_info = self._resolve_type()
        assert self._type_info is not None
        return self._type_info

    @property
    def state(self):
        return self._ensure_type_info()["state"]

    @property
    def file(self):
        return self._ensure_type_info()["file"]

    @property
    def status(self):
        return self._status

    @property
    def client_type_name(self):
        return str(self._client_type)

    @property
    def properties(self) -> List[PropertyBuilder]:
        return self._properties

    @property
    def members(self) -> List[MemberBuilder]:
        return self._members

    @property
    def entity_type_name(self) -> str:
        return self._schema.FullName
