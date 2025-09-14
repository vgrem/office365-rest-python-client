import ast
import importlib
import inspect
import os
import pkgutil
from functools import lru_cache
from os.path import abspath
from typing import Dict

import astunparse
from typing_extensions import Self

from generator.builders.template_context import TemplateContext
from office365.runtime.odata.type import ODataType


class TypeBuilder(ast.NodeTransformer):
    """Type builder"""

    def __init__(self, type_schema: ODataType, options: Dict[str, str] = None):
        self._schema = type_schema
        self._options = options
        self._type_info = None
        self._source_tree = None
        self._status = None

    def visit_ClassDef(self, node: ast.ClassDef):
        if self._schema:
            node.name = self._schema.className.title()

        if self._schema and self._schema.properties:
            for prop_name, prop_schema in self._schema.properties.items():
                prop_schema.status = "detached"

        self.generic_visit(node)

        return node

    def visit_FunctionDef(self, node):
        is_property = False
        for decorator in node.decorator_list:
            if (isinstance(decorator, ast.Name) and decorator.id == "property") or (
                isinstance(decorator, ast.Attribute) and decorator.attr == "property"
            ):
                is_property = True
                break

        if is_property:
            if node.name in self._schema.properties:
                self._schema.properties[node.name].status = "attached"

        return self.generic_visit(node)

    def build(self) -> Self:
        if self.state == "attached":
            with open(self.file, encoding="utf-8") as f:
                self._source_tree = ast.parse(f.read())
            self._status = "updated"
        else:
            template_ctx = TemplateContext(self._options.get("templatepath"))
            self._source_tree = template_ctx.build(self._schema)
            self._status = "created"
        self.visit(self._source_tree)
        return self

    def save(self):
        code = astunparse.unparse(self._source_tree)
        with open(self.file, "w", encoding="utf-8") as f:
            f.write(code)

    @lru_cache(maxsize=512)
    def _find_model_class(self, name: str):
        class_name = name.split(".")[-1]
        modules = [t.strip() for t in self._options["modules"].split(",")]

        for root_name in modules:
            try:
                base_pkg = importlib.import_module(root_name)
                for mod_info in pkgutil.walk_packages(
                    base_pkg.__path__, base_pkg.__name__ + "."
                ):
                    try:
                        module = importlib.import_module(mod_info.name)
                        if hasattr(module, class_name):
                            cls = getattr(module, class_name)
                            if inspect.isclass(cls):
                                return cls
                    except ImportError:
                        continue
            except ImportError:
                continue
        return None

    def _resolve_type(self, type_name: str) -> Dict[str, str]:
        type_info = {}

        cls = self._find_model_class(type_name)
        if cls is not None:
            type_info["state"] = "attached"
            type_info["file"] = inspect.getsourcefile(cls)
        else:
            type_info["state"] = "detached"
            type_info["file"] = abspath(
                os.path.join(self._options["outputpath"], type_name + ".py")
            )
        return type_info

    def _ensure_type_info(self):
        if self._type_info is None:
            self._type_info = self._resolve_type(self._schema.name)
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
