"""Two CSDL types sharing one module: which name the class answers with.

``descend_module`` names a file after the class's short name, so ``microsoft.graph.Alert``
and ``microsoft.graph.security.Alert`` both resolve to ``office365/security/alerts/alert.py``.
The file holds one class, and ``entity_type_name`` is written once (never overwritten by a
later run), so a class can answer for a member set it does not belong to. These tests pin
the decision the generator makes about that — and freeze the modules where it happens, so a
new collision is a failing test rather than a ``system=True`` marker on an inherited name.
"""

from __future__ import annotations

import ast
from functools import lru_cache
from pathlib import Path

from generator.builders import placement
from generator.builders.context import BuilderContext
from generator.builders.naming import normalize_member_key
from generator.builders.resolution import TypeRegistry
from generator.builders.type import TypeBuilder
from generator.config import GeneratorOptions
from generator.filters import TypeFilter
from generator.odata.property import PropertyInformation
from generator.odata.type_information import TypeInformation
from generator.routing import Router
from generator.services import get_service
from generator.type_identity import (
    audit,
    claimed_modules,
    class_spellings,
    entity_type_name_literal,
    identity_evidence,
    modelled_type,
)

_GENERATOR = Path(__file__).resolve().parents[2] / "generator"

#: One class, two candidate types; its members decide which it belongs to.
_WIDGET = """
class Widget(ClientValue):
    @property
    def entity_type_name(self):
        return "acme.gadget.Widget"

    @property
    def serial(self):
        return self.properties.get("serial", None)

    @property
    def colour(self):
        return self.properties.get("colour", None)
"""

#: Every type of the model: the candidate's names, and the name it answers with.
_PROPERTIES = {
    "acme.Widget": frozenset({"serial", "colour"}),
    "acme.gadget.Widget": frozenset({"serial"}),
}

#: The same class, but it also spells a name only the type it answers with declares.
_MERGED = """
class Widget(ClientValue):
    @property
    def entity_type_name(self):
        return "acme.gadget.Widget"

    @property
    def serial(self):
        return self.properties.get("serial", None)

    @property
    def colour(self):
        return self.properties.get("colour", None)

    @property
    def shade(self):
        return self.properties.get("shade", None)
"""

_MERGED_PROPERTIES = {
    "acme.Widget": frozenset({"serial", "colour"}),
    "acme.gadget.Widget": frozenset({"serial", "shade"}),
}


def _class(source: str) -> ast.ClassDef:
    node = ast.parse(source).body[0]
    assert isinstance(node, ast.ClassDef)
    return node


def _decide(node: ast.ClassDef, properties: dict[str, frozenset[str]], declared: str) -> str | None:
    return modelled_type(node, declared=declared, candidate="acme.Widget", declared_properties=properties)


def test_a_class_is_renamed_to_the_type_its_members_come_from() -> None:
    node = _class(_WIDGET)

    assert entity_type_name_literal(node) == "acme.gadget.Widget"
    assert _decide(node, _PROPERTIES, "acme.gadget.Widget") == "acme.Widget"
    # The witness is the one name the candidate declares and the current name does not.
    witness, refute = identity_evidence(
        node, declared="acme.gadget.Widget", candidate="acme.Widget", declared_properties=_PROPERTIES
    )
    assert (witness, refute) == (frozenset({"colour"}), frozenset())


def test_a_class_that_also_spells_its_own_name_members_is_not_renamed() -> None:
    node = _class(_MERGED)

    assert _decide(node, _MERGED_PROPERTIES, "acme.gadget.Widget") is None


def test_a_name_the_model_does_not_contain_is_still_correctable() -> None:
    """Nothing can refute a type that declares nothing, so the witness decides alone."""
    node = _class(_WIDGET)

    assert _decide(node, {"acme.Widget": _PROPERTIES["acme.Widget"]}, "acme.gadget.Widget") == "acme.Widget"


def test_a_class_that_spells_no_member_is_left_alone() -> None:
    """An enum (or an empty scaffold) has no members to be evidence with."""
    node = _class(
        """
class Severity(Enum):
    @property
    def entity_type_name(self):
        return "acme.gadget.Severity"
"""
    )

    assert class_spellings(node) == frozenset()
    assert _decide(node, _PROPERTIES, "acme.gadget.Severity") is None


def test_the_same_type_spelled_otherwise_is_not_a_rename() -> None:
    """The model key Pascal-cases the CSDL's last segment; the wire name need not be.

    ``Microsoft.SharePoint.Comments.comment`` reads as ``...Comments.Comment`` in the
    model, and a class answers with the spelling the service uses -- one type, two
    spellings, so there is nothing to rename.
    """
    node = _class(
        """
class Comment(Entity):
    @property
    def entity_type_name(self):
        return "SP.Comments.comment"
"""
    )

    assert (
        modelled_type(
            node,
            declared="SP.Comments.comment",
            candidate="SP.Comments.Comment",
            declared_properties={"SP.Comments.Comment": frozenset({"text"})},
        )
        is None
    )


def test_a_name_the_type_already_answers_is_not_a_correction() -> None:
    node = _class(_WIDGET)

    assert _decide(node, _PROPERTIES, "acme.Widget") is None


def test_audit_names_the_verdict_per_shared_module(tmp_path: Path) -> None:
    module = "acme.widget"
    package = tmp_path / "acme"
    package.mkdir()
    (package / "widget.py").write_text(_MERGED, encoding="utf-8")

    claims = {module: ("acme.Widget", "acme.gadget.Widget")}
    rows = audit(claims, {}, _MERGED_PROPERTIES, root=str(tmp_path))

    assert [(row.class_name, row.verdict) for row in rows] == [("Widget", "merged")]


#: Modules claimed by more than one type of the shipped Graph snapshot, frozen.
#: ``agrees`` -- the class answers with the type its members come from; the two
#: names are one concept in two namespaces (mostly enums, whose members are values,
#: not columns, so nothing distinguishes them). ``unnamed`` -- the file declares no
#: ``entity_type_name`` at all. ``grouped`` -- two classes, one per type, on purpose.
#: ``merged`` -- known defect: the class grew both types' members and can only answer
#: for one of them (a placement question, not a renaming one; see slice D).
_FROZEN_CLAIMS: dict[str, tuple[tuple[str, str], ...]] = {
    "office365.backuprestore.service_status": (
        "microsoft.graph.ServiceStatus",
        "microsoft.graph.security.ServiceStatus",
    ),
    "office365.communications.callrecords.media_stream": (
        "microsoft.graph.MediaStream",
        "microsoft.graph.callRecords.MediaStream",
    ),
    "office365.communications.callrecords.modality": (
        "microsoft.graph.Modality",
        "microsoft.graph.callRecords.Modality",
    ),
    "office365.directory.audit.logs.recordtype": (
        "microsoft.graph.AuditLogRecordType",
        "microsoft.graph.security.AuditLogRecordType",
    ),
    "office365.directory.audit.logs.usertype": (
        "microsoft.graph.AuditLogUserType",
        "microsoft.graph.security.AuditLogUserType",
    ),
    "office365.directory.extensions.extended_property": (
        "microsoft.graph.MultiValueLegacyExtendedProperty",
        "microsoft.graph.SingleValueLegacyExtendedProperty",
    ),
    "office365.directory.identities.container": (
        "microsoft.graph.IdentityContainer",
        "microsoft.graph.security.IdentityContainer",
    ),
    "office365.security.alerts.alert": ("microsoft.graph.Alert", "microsoft.graph.security.Alert"),
    "office365.security.alerts.severity": ("microsoft.graph.AlertSeverity", "microsoft.graph.security.AlertSeverity"),
    "office365.security.alerts.status": ("microsoft.graph.AlertStatus", "microsoft.graph.security.AlertStatus"),
    "office365.security.dictionary": ("microsoft.graph.Dictionary", "microsoft.graph.security.Dictionary"),
    "office365.security.file_hash": ("microsoft.graph.FileHash", "microsoft.graph.security.FileHash"),
}

#: Why each frozen module is shared. Anything not ``agrees`` needs a human decision.
_FROZEN_VERDICTS: dict[str, tuple[str, ...]] = {
    "office365.directory.extensions.extended_property": ("unnamed", "unnamed"),
    "office365.directory.identities.container": ("merged",),
    "office365.security.alerts.alert": ("merged",),
    "office365.security.dictionary": ("unnamed",),
}


class _StubResolver:
    """Marks the type attached without indexing the tree."""

    def resolve(self, type_name):
        return None

    def module_for(self, type_name):
        return "acme.widget"

    def strict_module_for(self, type_name, kind=None):
        return "acme.widget"

    def members_of(self, type_name):
        return set()


def _builder(tmp_path: Path, properties: dict[str, frozenset[str]]) -> TypeBuilder:
    schema = TypeInformation(BaseTypeFullName="EntityType", FullName="acme.Widget", IsValueObject=False)
    schema.add_property(PropertyInformation(Name="serial", TypeName="Edm.String"))
    schema.add_property(PropertyInformation(Name="colour", TypeName="Edm.String"))
    context = BuilderContext(output_path=str(tmp_path), modules="acme", declared_properties=properties)
    return TypeBuilder(schema, context, resolver=_StubResolver())


def test_the_generated_class_answers_with_the_type_its_members_come_from(tmp_path: Path, monkeypatch) -> None:
    target = tmp_path / "widget.py"
    target.write_text(_WIDGET, encoding="utf-8")
    monkeypatch.setattr(placement, "module_file", lambda name: str(target))

    builder = _builder(tmp_path, _PROPERTIES)
    builder.build()
    builder.save()

    source = target.read_text(encoding="utf-8")
    assert 'return "acme.Widget"' in source
    assert "acme.gadget.Widget" not in source


def test_a_merged_class_keeps_the_name_it_answers_with(tmp_path: Path, monkeypatch) -> None:
    target = tmp_path / "widget.py"
    target.write_text(_MERGED, encoding="utf-8")
    monkeypatch.setattr(placement, "module_file", lambda name: str(target))

    builder = _builder(tmp_path, _MERGED_PROPERTIES)
    builder.build()
    builder.save()

    assert 'return "acme.gadget.Widget"' in target.read_text(encoding="utf-8")


@lru_cache(maxsize=None)
def _graph_tree() -> tuple[dict[str, tuple[str, ...]], list[tuple[str, str, str]]]:
    options = GeneratorOptions.load("graph", _GENERATOR)
    model = get_service("graph").reader(options.metadata_path).read()
    schema_filter = TypeFilter.from_options(options)
    registry = TypeRegistry(options.modules.split(","), namespace=options.namespace)
    router = Router.from_options(options.builder_context())
    declared_properties = {
        name: frozenset(normalize_member_key(key) for key in keys)
        for name, keys in model.effective_property_names().items()
    }
    claims = claimed_modules(
        model,
        registry=registry,
        router=router,
        output_path=options.output_path,
        in_scope=schema_filter.in_scope,
    )
    rows = audit(claims, {}, declared_properties)
    return dict(claims), [(row.module, row.class_name, row.verdict) for row in rows]


def test_shared_modules_are_the_frozen_ones() -> None:
    claims, _ = _graph_tree()

    assert claims == _FROZEN_CLAIMS


def test_no_shared_module_is_provably_misnamed() -> None:
    _, rows = _graph_tree()

    assert [row for row in rows if row[2] == "misnamed"] == []


def test_a_reviewed_shared_module_keeps_its_verdict() -> None:
    _, rows = _graph_tree()

    verdicts: dict[str, list[str]] = {}
    for module, _, verdict in rows:
        verdicts.setdefault(module, []).append(verdict)
    assert verdicts == {module: list(_FROZEN_VERDICTS.get(module, ("agrees",))) for module in _FROZEN_CLAIMS}
