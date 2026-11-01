"""Golden tests: hand-written code in a generated model survives regeneration.

The generator updates files in place (it never re-creates a type), so custom
methods, properties and decorator arguments must be left untouched while new
metadata members are still added, and a repeated run must be a no-op.
"""

from __future__ import annotations

import ast
from pathlib import Path

from generator.odata.v3.metadata_reader import ODataV3Reader
from tests.tooling.test_generator_e2e import _V3_CSDL, _options, _run

_CUSTOM_METHOD = '''
    def custom_method(self, value):
        """Hand-written: must survive regeneration."""
        return self.get_property("Title", value)
'''

_CUSTOM_PROPERTY = '''
    @property
    def custom_label(self):
        """Hand-written property."""
        return self.properties.get("Title", None)
'''


def _generate(tmp_path: Path):
    metadata = tmp_path / "metadata.xml"
    metadata.write_text(_V3_CSDL, encoding="utf-8")
    options = _options(tmp_path, graph=False, namespace="SP", kinds=["EntityType"], prefix="SP")
    _run(options, ODataV3Reader, tmp_path)
    return metadata, options, tmp_path / "office365" / "widget.py"


def _with_new_property(metadata: Path) -> None:
    metadata.write_text(
        _V3_CSDL.replace(
            '<Property Name="Title"', '<Property Name="Note" Type="Edm.String" />\n        <Property Name="Title"'
        ),
        encoding="utf-8",
    )


def test_custom_members_survive_regeneration(tmp_path: Path) -> None:
    metadata, options, widget = _generate(tmp_path)
    widget.write_text(widget.read_text(encoding="utf-8").rstrip("\n") + "\n" + _CUSTOM_METHOD + _CUSTOM_PROPERTY)

    _with_new_property(metadata)
    _run(options, ODataV3Reader, tmp_path, force=True)
    after = widget.read_text(encoding="utf-8")
    ast.parse(after)

    assert '"Note"' in after  # new member added
    assert "def custom_method(self, value):" in after
    assert '"""Hand-written: must survive regeneration."""' in after
    assert "def custom_label(self):" in after
    assert after.count("def custom_method") == 1
    assert after.count("def custom_label") == 1


def test_custom_decorator_arguments_survive_regeneration(tmp_path: Path) -> None:
    metadata, options, widget = _generate(tmp_path)
    source = widget.read_text(encoding="utf-8")
    assert '@odata(name="Title")' in source
    widget.write_text(source.replace('@odata(name="Title")', '@odata(name="Title", readonly=True)'))

    _with_new_property(metadata)
    _run(options, ODataV3Reader, tmp_path, force=True)
    after = widget.read_text(encoding="utf-8")

    assert '@odata(name="Title", readonly=True)' in after
    assert after.count('name="Title"') == 1  # not duplicated by the update


def test_second_run_is_a_noop(tmp_path: Path) -> None:
    metadata, options, widget = _generate(tmp_path)
    widget.write_text(widget.read_text(encoding="utf-8").rstrip("\n") + "\n" + _CUSTOM_METHOD)
    _with_new_property(metadata)
    _run(options, ODataV3Reader, tmp_path, force=True)
    first = widget.read_text(encoding="utf-8")

    _run(options, ODataV3Reader, tmp_path, force=True)

    assert widget.read_text(encoding="utf-8") == first


def test_new_field_before_a_multiline_field_keeps_source_valid(tmp_path: Path) -> None:
    from generator.edit.source_editor import SourceEditor

    assert hasattr(SourceEditor, "_field_slot")
    fields = [("accessToken", 3, 3), ("saml2Token", 4, 6)]
    member = ast.parse("kerberosTicket: int = 0").body[0]

    # Inserted before the first line of the next field (0-based index 3), not inside it.
    expected = fields[1][1] - 1
    assert SourceEditor._field_slot(fields, member) == expected
