"""A column's ``SchemaXml`` edited as XML rather than as text.

``SchemaXml`` is the ``FieldDefinition`` element of ``[MS-WSSFO2] 2.2.8.3.3.1``: 142
attributes, 13 child elements, ``xs:anyAttribute``, and a ``Customization`` element
declared ``processContents="skip"``. The parts a caller edits are two root attributes
(the ``List`` a lookup resolves against, and the ``SourceID``/``Version`` pair that
names where the definition came from); everything else has to survive untouched,
which is why this edits a parsed tree instead of running a regular expression over
the string. On a tenant with 7,751 field schemas, all of them parse, and 28 distinct
attributes appear that the published schema does not declare -- so the tree is
carried as found rather than validated against the spec.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Optional
from xml.etree import ElementTree

#: The attributes that name a definition's *origin*: the web/list it was copied from
#: and that copy's schema version. Replaying them elsewhere is rejected by the
#: service ("The object has been updated by another user since it was last fetched").
ORIGIN_ATTRIBUTES = ("SourceID", "Version")

#: The attribute a lookup column uses to name the list it resolves against.
LIST_ATTRIBUTE = "List"


class FieldSchema:
    """One parsed ``SchemaXml``.

    Instances are values: every edit returns a new schema, so a reader may hand the
    same object to several consumers without one of them changing what the next sees.
    """

    __slots__ = ("_root",)

    def __init__(self, root: ElementTree.Element) -> None:
        self._root = root

    @classmethod
    def parse(cls, schema_xml: Optional[str]) -> Optional["FieldSchema"]:
        """Parse a schema, or answer ``None`` when there is none to parse.

        Raises:
            ValueError: if the schema is not well-formed XML. An unreadable schema
                cannot be edited, and returning it unedited is how a column ends up
                copied with the ids this module exists to take out.
        """
        if not schema_xml:
            return None
        try:
            root = ElementTree.fromstring(schema_xml)
        except ElementTree.ParseError as exc:
            raise ValueError(f"SchemaXml is not well-formed XML ({exc})") from exc
        return cls(root)

    @property
    def type_name(self) -> Optional[str]:
        """The column's ``Type`` spelling (``Lookup``, ``Choice``, ...)."""
        return self._root.get("Type")

    @property
    def list_id(self) -> Optional[str]:
        """The ``List`` this schema names, in the spelling it carries (braces kept).

        Only the root is read: a ``<FieldRef List="...">`` descendant names a *view*
        or content-type membership, not the list the column resolves against.
        """
        return self._root.get(LIST_ATTRIBUTE)

    def without_origin_attributes(self) -> "FieldSchema":
        """A copy that names no origin, portable to another site."""
        root = deepcopy(self._root)
        for name in ORIGIN_ATTRIBUTES:
            root.attrib.pop(name, None)
        return FieldSchema(root)

    def with_list(self, list_id: str) -> "FieldSchema":
        """A copy that resolves against ``list_id``.

        Args:
            list_id (str): A normalized list id -- no braces, as
                :func:`office365.migration.identity.normalize_guid` answers it. The
                braces the attribute is spelled with are added here.
        """
        root = deepcopy(self._root)
        root.set(LIST_ATTRIBUTE, f"{{{list_id}}}")
        return FieldSchema(root)

    def to_xml(self) -> str:
        """The schema as the service takes it back."""
        return ElementTree.tostring(self._root, encoding="unicode")
