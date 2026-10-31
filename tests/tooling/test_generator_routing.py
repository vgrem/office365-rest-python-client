"""Offline tests for the layered router (namespace, exact type, prefix, inference)
and the Graph docs service taxonomy that seeds it."""

from __future__ import annotations

import json
from pathlib import Path

from generator.builders.context import BuilderContext
from generator.builders.resolution import TypeRegistry
from generator.documentation import subservices
from generator.filters import TypeFilter
from generator.odata.model import ODataModel
from generator.odata.property import PropertyInformation
from generator.odata.type_information import TypeInformation
from generator.routing import Router, infer_placements, render_suggestions, route_namespace


def test_infer_placements_propagates_from_routed_anchors():
    """A routed type's module spreads to the types it references."""
    model = ODataModel()
    anchor = TypeInformation(BaseTypeFullName="EntityType", FullName="SP.A", IsValueObject=False)
    anchor.add_property(PropertyInformation(Name="b", TypeName="SP.B"))
    referenced = TypeInformation(BaseTypeFullName="ComplexType", FullName="SP.B", IsValueObject=True)
    model.add_type(anchor)
    model.add_type(referenced)
    router = Router(types={"SP.A": "office365.a"})

    assigned = infer_placements(model, TypeFilter(include_base_types=set()), TypeRegistry([]), router)

    assert assigned["SP.A"] == "office365.a"
    assert assigned["SP.B"] == "office365.a"  # inferred from its only referrer


def test_route_namespace_sanitizes_non_identifier_segments():
    routing = {"microsoft.graph.deviceManagement": "office365.intune"}

    assert route_namespace("microsoft.graph.deviceManagement.windows.10", routing) == "office365.intune.windows._10"
    assert route_namespace("microsoft.graph.deviceManagement.class", routing) == "office365.intune._class"


def test_route_namespace_longest_prefix_wins():
    routing = {"SP": "office365.sharepoint", "SP.Directory": "office365.sharepoint.directory"}
    assert route_namespace("SP.Directory.Provider", routing) == "office365.sharepoint.directory.provider"
    assert route_namespace("SP.Web", routing) == "office365.sharepoint.web"
    assert route_namespace("Other.Thing", routing) == ""


def test_router_prefers_exact_then_namespace_then_prefix():
    router = Router(
        namespace={"microsoft.graph.security": "office365.security"},
        types={"microsoft.graph.Special": "office365.special", "Edu*": "office365.education"},
    )
    assert router.module_for("microsoft.graph.Special") == "office365.special"  # exact
    assert router.module_for("microsoft.graph.security.Alert") == "office365.security"  # namespace
    assert router.module_for("microsoft.graph.EduThing") == "office365.education"  # prefix
    assert router.module_for("microsoft.graph.Unknown") is None  # unrouted


def test_router_from_options():
    router = Router.from_options(
        BuilderContext(
            output_path="",
            routing={"SP": " office365.sharepoint "},
            type_routing={"microsoft.graph.KeyValue": "office365.common"},
        )
    )
    assert router.namespace == {"SP": "office365.sharepoint"}
    assert router.module_for("microsoft.graph.KeyValue") == "office365.common"


def test_short_name_exact_rule_matches_bare_type():
    router = Router(types={"AlertDetection": "office365.security"})
    assert router.module_for("microsoft.graph.AlertDetection") == "office365.security"


def test_short_exact_rule_does_not_override_prefix_for_named_namespace():
    router = Router(
        namespace={"microsoft.graph.search": "office365.search"},
        types={"SearchRequest": "office365.other"},
    )
    assert router.module_for("microsoft.graph.search.SearchRequest") == "office365.search"
    assert router.module_for("microsoft.graph.SearchRequest") == "office365.other"


def test_router_fallback_and_bucket_detection():
    from generator.routing import _in_fallback

    router = Router(types={"*": "office365.common"})
    assert router.fallback == "office365.common"
    assert _in_fallback("office365.common.workbook_chart_axis_format", router.fallback)
    assert not _in_fallback("office365.directory.user", router.fallback)


def test_prefix_specificity_does_not_depend_on_table_order():
    """A narrower prefix wins wherever the table happens to spell it."""
    narrow_first = Router(types={"Printer*": "office365.printers", "Print*": "office365.print"})
    narrow_last = Router(types={"Print*": "office365.print", "Printer*": "office365.printers"})

    for router in (narrow_first, narrow_last):
        assert router.module_for("microsoft.graph.PrinterShare") == "office365.printers"
        assert router.module_for("microsoft.graph.PrintJob") == "office365.print"


def test_catch_all_answers_only_after_every_prefix_rule_declines():
    """``*`` means "everything else", not "everything from here on"."""
    router = Router(types={"*": "office365.common", "Foo*": "office365.foo"})

    assert router.module_for("microsoft.graph.FooBar") == "office365.foo"
    assert router.module_for("microsoft.graph.Bar") == "office365.common"
    assert router.module_for("microsoft.graph.Bar", allow_fallback=False) is None


def test_owning_module_prefers_ancestor_of_the_dominant_referrer():
    from collections import Counter

    from generator.routing import _owning_module

    modules = Counter({"office365.intune.x.app.protections": 3, "office365.intune.x.app": 1})
    assert _owning_module(modules) == "office365.intune.x.app"


# --------------------------------------------------------------- service taxonomy


def test_write_and_load_service_map(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(subservices, "_CACHE_PATH", tmp_path / "graph_services.json")

    assert subservices.load_service_map() == {}
    subservices.write_service_map({"user": "users", "alert": "security"})

    assert subservices.load_service_map() == {"alert": "security", "user": "users"}


def test_fetch_service_map_parses_resource_links(monkeypatch) -> None:
    def fake_get(url: str) -> str:
        if "/contents/" in url:
            return json.dumps([{"name": "users", "type": "dir"}, {"name": "README.md", "type": "file"}])
        return "- name: User\n  href: ../../resources/user.md\n- name: x\n  href: ../../api/user-get.md\n"

    monkeypatch.setattr(subservices, "_get", fake_get)

    assert subservices.fetch_service_map() == {"user": "users"}


def test_render_suggestions_prefers_the_service_taxonomy() -> None:
    model = ODataModel()
    model.add_type(
        TypeInformation(BaseTypeFullName="EntityType", FullName="microsoft.graph.Widget", IsValueObject=False)
    )

    suggestions = render_suggestions(
        model,
        TypeFilter(include_base_types=set()),
        TypeRegistry([]),
        Router(),
        services={"gadgets": "office365.gadgets"},
        service_map={"widget": "gadgets"},
    )

    assert '"Widget": office365.gadgets   # service: gadgets' in suggestions
