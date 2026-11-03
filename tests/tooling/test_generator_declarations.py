"""The declaration rules the generator runs over the model (``python -m generator verify``)."""

from __future__ import annotations

import textwrap
from pathlib import Path

from generator.tools.declarations import (
    declaration_report,
    navigation_disagreements,
    untyped_columns,
    witness_disagreements,
)


def _model(tmp_path: Path, name: str, module: str, source: str) -> Path:
    """A throwaway model tree, importable under its own name (no clash with ``office365``)."""
    package = tmp_path / name
    (package / "probe").mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "probe" / "__init__.py").write_text("", encoding="utf-8")
    (package / "probe" / f"{module}.py").write_text(textwrap.dedent(source), encoding="utf-8")
    return package


def test_the_rendered_model_answers_every_rule():
    # Floors on how many subjects each rule reached are the tool's own findings: a rule
    # whose subjects stopped resolving reports ok while checking nothing.
    report = declaration_report()
    assert report.ok, report.render()


def test_a_getter_that_reads_another_name_is_reported(tmp_path):
    package = _model(
        tmp_path,
        "fixture_witness",
        "event",
        """
        from office365.runtime.types.odata_property import odata


        class Event:
            @odata(name="iCalUId")
            @property
            def ical_uid(self):
                return self.properties.get("icalUid", None)
        """,
    )

    findings, _ = witness_disagreements(package)

    assert findings == ["probe/event.py Event.ical_uid declares 'iCalUId', reads ['icalUid']"]


def test_a_getter_that_reads_nothing_makes_no_claim(tmp_path):
    package = _model(
        tmp_path,
        "fixture_silent",
        "event",
        """
        from office365.runtime.types.odata_property import odata


        class Event:
            @odata(name="iCalUId")
            @property
            def ical_uid(self):
                return self.properties["iCalUId"]
        """,
    )

    findings, _ = witness_disagreements(package)

    assert findings == []


def test_a_column_without_a_declared_type_is_reported(tmp_path, monkeypatch):
    package = _model(
        tmp_path,
        "fixture_untyped",
        "item",
        """
        from office365.runtime.client_object import ClientObject
        from office365.runtime.types.odata_property import odata


        class Item(ClientObject):
            @odata(name="Typed")
            @property
            def typed(self) -> str:
                return self.properties.get("Typed", None)

            @odata(name="Untyped")
            @property
            def untyped(self):
                return self.properties.get("Untyped", None)
        """,
    )
    monkeypatch.syspath_prepend(str(tmp_path))

    findings, _ = untyped_columns(package)

    assert findings == ["fixture_untyped.probe.item.Item.Untyped"]


def test_a_client_object_declared_as_a_column_is_reported(tmp_path, monkeypatch):
    package = _model(
        tmp_path,
        "fixture_navigation",
        "item",
        """
        from office365.runtime.client_object import ClientObject
        from office365.runtime.client_value import ClientValue
        from office365.runtime.types.odata_property import odata


        class Child(ClientObject):
            pass


        class Value(ClientValue):
            pass


        class Item(ClientObject):
            @odata(name="Expanded", navigation=True)
            @property
            def expanded(self) -> Child:
                return self.properties.get("Expanded", None)

            @odata(name="Column")
            @property
            def column(self) -> Child:
                return self.properties.get("Column", None)

            @odata(name="Hydrated", navigation=True)
            @property
            def hydrated(self) -> Value:
                return self.properties.get("Hydrated", None)
        """,
    )
    monkeypatch.syspath_prepend(str(tmp_path))

    findings, _ = navigation_disagreements(package)

    # The value-typed getter on a declared navigation is not reported: SharePoint v3
    # hydrates a navigation as a value.
    assert findings == ["fixture_navigation.probe.item.Item.column: a client object declared as a column"]
