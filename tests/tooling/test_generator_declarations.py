"""The generator's own declaration check: ``python -m generator verify``.

The rules are internal to the generator, so this is the floor under them, not a spec:
a model that breaks them is reported. The sweep *over this repo's model* is not
repeated here -- ``python -m generator verify`` is that test, and CI runs it as its
own job (``.github/workflows/ci.yml``); what is pinned here is that the check can
actually fail.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

from generator.tools.declarations import (
    navigation_disagreements,
    untyped_columns,
    witness_disagreements,
)


def _model(tmp_path: Path, source: str) -> Path:
    """A throwaway model tree, importable under its own name (no clash with ``office365``)."""
    package = tmp_path / "fixture_model"
    (package / "probe").mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "probe" / "__init__.py").write_text("", encoding="utf-8")
    (package / "probe" / "item.py").write_text(textwrap.dedent(source), encoding="utf-8")
    return package


def test_a_model_that_breaks_the_rules_is_reported(tmp_path, monkeypatch):
    package = _model(
        tmp_path,
        """
        from office365.runtime.client_object import ClientObject
        from office365.runtime.types.odata_property import odata


        class Child(ClientObject):
            pass


        class Item(ClientObject):
            @odata(name="iCalUId")
            @property
            def ical_uid(self) -> str:
                return self.properties.get("icalUid", None)

            @odata(name="Untyped")
            @property
            def untyped(self):
                return self.properties.get("Untyped", None)

            @odata(name="Column")
            @property
            def column(self) -> Child:
                return self.properties.get("Column", None)
        """,
    )
    monkeypatch.syspath_prepend(str(tmp_path))

    witness, _ = witness_disagreements(package)
    untyped, _ = untyped_columns(package)
    navigation, _ = navigation_disagreements(package)

    assert witness == ["probe/item.py Item.ical_uid declares 'iCalUId', reads ['icalUid']"]
    assert untyped == ["fixture_model.probe.item.Item.Untyped"]
    assert navigation == ["fixture_model.probe.item.Item.column: a client object declared as a column"]
