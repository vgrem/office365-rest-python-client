"""Typed CAML ``<FieldRef>`` nodes."""

from __future__ import annotations

from typing import Optional
from xml.sax.saxutils import quoteattr


class FieldRef:
    """A CAML ``<FieldRef>`` element.

    ``Ascending``/``Collapse`` apply inside ``<OrderBy>``/``<GroupBy>``;
    ``LookupId``/``RefType``/``List`` support lookup and join clauses.
    """

    def __init__(
        self,
        name: str,
        *,
        ascending: Optional[bool] = None,
        collapse: Optional[bool] = None,
        nullable: Optional[bool] = None,
        lookup_id: bool = False,
        ref_type: Optional[str] = None,
        list_alias: Optional[str] = None,
    ) -> None:
        self.name = name
        self.ascending = ascending
        self.collapse = collapse
        self.nullable = nullable
        self.lookup_id = lookup_id
        self.ref_type = ref_type
        self.list_alias = list_alias

    def asc(self) -> "FieldRef":
        """A copy sorted ascending (for ``<OrderBy>``)."""
        return self._copy(ascending=True)

    def desc(self) -> "FieldRef":
        """A copy sorted descending (for ``<OrderBy>``)."""
        return self._copy(ascending=False)

    def _copy(self, **overrides) -> "FieldRef":
        return FieldRef(
            self.name,
            ascending=overrides.get("ascending", self.ascending),
            collapse=overrides.get("collapse", self.collapse),
            nullable=overrides.get("nullable", self.nullable),
            lookup_id=self.lookup_id,
            ref_type=self.ref_type,
            list_alias=self.list_alias,
        )

    def to_xml(self) -> str:
        attrs = [f"Name={quoteattr(self.name)}"]
        if self.ascending is not None:
            attrs.append(f'Ascending="{str(self.ascending).upper()}"')
        if self.collapse is not None:
            attrs.append(f'Collapse="{str(self.collapse).upper()}"')
        if self.nullable is not None:
            attrs.append(f'Nullable="{str(self.nullable).upper()}"')
        if self.lookup_id:
            attrs.append('LookupId="TRUE"')
        if self.ref_type is not None:
            attrs.append(f"RefType={quoteattr(self.ref_type)}")
        if self.list_alias is not None:
            attrs.append(f"List={quoteattr(self.list_alias)}")
        return f"<FieldRef {' '.join(attrs)}/>"
