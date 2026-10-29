"""Low-level traversal over a parsed CSDL (OData metadata) document.

Owns the XML namespaces, the schema ``Alias -> Namespace`` map, and namespace
qualification — the parts of reading that have nothing to do with building the
Python model.
"""

from __future__ import annotations

from typing import Dict, Optional
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element

from generator.odata.type_system import TypeRef, normalize_class_name

#: CSDL annotation term that declares alternate keys on an entity type.
_ALTERNATE_KEYS_TERM = "Org.OData.Core.V1.AlternateKeys"

#: CSDL annotation term for a member the service assigns, not the client.
_COMPUTED_TERM = "Org.OData.Core.V1.Computed"


class CsdlDocument:
    """Namespaces, schema aliases and traversal for one CSDL document."""

    def __init__(self, root: Element, namespaces: Dict[str, str]) -> None:
        self._root = root
        self._namespaces = namespaces
        self._aliases = self._load_aliases()

    @classmethod
    def load(cls, path: str, namespaces: Dict[str, str]) -> "CsdlDocument":
        """Parse a metadata file and wrap its root element."""
        return cls(ET.parse(path).getroot(), namespaces)

    @property
    def root(self) -> Element:
        return self._root

    @property
    def namespaces(self) -> Dict[str, str]:
        return self._namespaces

    def schemas(self) -> list[Element]:
        """The ``<Schema>`` elements of the document."""
        return self.findall("edmx:DataServices/xmlns:Schema")

    def findall(self, path: str) -> list[Element]:
        return self._root.findall(path, self._namespaces)

    def find(self, path: str) -> Optional[Element]:
        return self._root.find(path, self._namespaces)

    def _load_aliases(self) -> Dict[str, str]:
        """The ``Alias -> Namespace`` map declared by the schemas (e.g. ``graph``)."""
        aliases: Dict[str, str] = {}
        for schema_node in self.schemas():
            namespace = schema_node.get("Namespace")
            alias = schema_node.get("Alias")
            if namespace and alias:
                aliases[alias] = namespace
        return aliases

    def qualified_type_name(self, type_name: Optional[str]) -> Optional[str]:
        """Expand a schema alias to its namespace and normalize the class name.

        Graph metadata refers to types with aliases (``graph.user``,
        ``self.alertEvidence``); normalizing here keeps every ``TypeName``
        fully-qualified, so resolution and routing are unambiguous.
        """
        if not type_name:
            return type_name
        ref = TypeRef.parse(type_name)
        if ref.is_collection:
            return TypeRef(self.qualified_type_name(ref.name), is_collection=True).text
        namespace, sep, class_name = type_name.rpartition(".")
        if not sep or namespace == "Edm":
            return type_name
        namespace = self._aliases.get(namespace, namespace)
        return f"{namespace}.{normalize_class_name(class_name)}"

    def parse_alternate_keys(self, node: Element) -> list[tuple[str, ...]]:
        """Alternate keys declared on a type node.

        ``Org.OData.Core.V1.AlternateKeys`` is a collection of ``AlternateKey``
        records, each holding a ``Key`` collection of ``PropertyRef`` records.
        The property path lives in the ``Name`` ``PropertyValue``; returns one
        tuple of property names per declared key (empty when none).
        """
        result: list[tuple[str, ...]] = []
        for annotation in node.findall("xmlns:Annotation", self._namespaces):
            if annotation.get("Term") != _ALTERNATE_KEYS_TERM:
                continue
            for record in annotation.findall("xmlns:Collection/xmlns:Record", self._namespaces):
                for prop_value in record.findall("xmlns:PropertyValue", self._namespaces):
                    if prop_value.get("Property") != "Key":
                        continue
                    names: list[str] = []
                    refs = prop_value.findall("xmlns:Collection/xmlns:Record", self._namespaces)
                    for prop_ref in refs:
                        name = self._property_ref_name(prop_ref)
                        if name:
                            names.append(name)
                    if names:
                        result.append(tuple(names))
        return result

    def parse_entity_key(self, node: Element) -> tuple[str, ...]:
        """The properties an entity type's identity is spelled with (CSDL ``<Key>``).

        ``<Key>`` holds one ``<PropertyRef>`` per member, in declaration order. A derived
        type declares none and inherits its base's, which is why the answer is empty on
        most types: it means the document states nothing, not that the type has no key.
        """
        declared = node.find("xmlns:Key", self._namespaces)
        if declared is None:
            return ()
        return tuple(
            name for name in (ref.get("Name") for ref in declared.findall("xmlns:PropertyRef", self._namespaces)) if name
        )

    def _property_ref_name(self, prop_ref: Element) -> Optional[str]:
        """The property path of a ``PropertyRef`` record (its ``Name`` value)."""
        for prop_value in prop_ref.findall("xmlns:PropertyValue", self._namespaces):
            if prop_value.get("Property") == "Name":
                return prop_value.get("PropertyPath")
        return None

    def parse_computed_members(self) -> set[tuple[str, str]]:
        """Members the service assigns rather than the client (``Core.Computed``).

        Graph writes these on schema-level ``<Annotations Target="Type/member">``
        blocks, never on the property element, so the fact exists only here --
        reading a ``<Property>`` node alone can never tell that the service owns
        its value. The target's type part is qualified like any other type
        reference, so an aliased target matches the type's own ``FullName``.
        """
        declared: set[tuple[str, str]] = set()
        for schema in self.schemas():
            for block in schema.findall("xmlns:Annotations", self._namespaces):
                terms = {node.get("Term") for node in block.findall("xmlns:Annotation", self._namespaces)}
                if _COMPUTED_TERM not in terms:
                    continue
                target = block.get("Target") or ""
                type_name, sep, member = target.rpartition("/")
                if not sep or not member or member == "$Kind":
                    continue
                qualified = self.qualified_type_name(type_name)
                if qualified:
                    declared.add((qualified, member))
        return declared

    def parse_parameters(self, node: Element) -> list:
        """Extract ``<Parameter>`` children into plain dicts (types qualified)."""
        return [
            {
                "Name": param.get("Name"),
                "Type": self.qualified_type_name(param.get("Type")),
                "Nullable": param.get("Nullable") != "false",
            }
            for param in node.findall("xmlns:Parameter", self._namespaces)
        ]

    def entity_anchors(self) -> dict[str, str]:
        """The root container name (entity set / singleton) for each root type.

        E.g. ``users -> microsoft.graph.User``, ``identityGovernance ->
        microsoft.graph.identityGovernance``. These anchor otherwise-unreferenced
        root types to a product area, for routing suggestions.
        """
        anchors: dict[str, str] = {}
        for container in self.findall("edmx:DataServices/xmlns:Schema/xmlns:EntityContainer"):
            for node in container.findall("xmlns:EntitySet", self._namespaces):
                type_name = self.qualified_type_name(node.get("EntityType"))
                if type_name:
                    anchors.setdefault(type_name, node.get("Name") or "")
            for node in container.findall("xmlns:Singleton", self._namespaces):
                type_name = self.qualified_type_name(node.get("Type"))
                if type_name:
                    anchors.setdefault(type_name, node.get("Name") or "")
        return anchors
