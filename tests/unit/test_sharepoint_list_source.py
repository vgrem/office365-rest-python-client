"""Offline tests: taxonomy fallback in the SharePoint list source and the
assessment classification of the orphaned-term-set failure."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from office365.migration import ConflictResolution, MigrationAssessor, MigrationJob, MigrationOptions
from office365.migration.adapters.filesystem import JsonFileTarget
from office365.migration.assessment.report import AssessmentReport
from office365.migration.sharepoint.adapters import (
    SharePointListSource,
    is_taxonomy_validation,
    taxonomy_internal_names,
)

if TYPE_CHECKING:
    from office365.sharepoint.folders.folder import Folder
    from office365.sharepoint.lists.list import List as SPList
    from office365.sharepoint.webs.web import Web


class _Item:
    def __init__(self, item_id: int, properties: dict):
        self.id = item_id
        self.properties = properties


class _Field:
    def __init__(self, internal_name: str, type_as_string: str = "", schema_xml: str = "", hidden: bool = False):
        self.internal_name = internal_name
        self.type_as_string = type_as_string
        self.schema_xml = schema_xml
        self.hidden = hidden


class _Query:
    def __init__(self, load, select):
        self._load = load
        self._select = select

    def execute_query(self):
        return self._load(self._select)


class _ItemsEndpoint:
    def __init__(self, load):
        self._load = load
        self._select = None

    def select(self, columns: list[str]):
        self._select = columns
        return self

    def get_all(self):
        return _Query(self._load, self._select)


class _List:
    def __init__(self, title: str, load, fields: list[_Field]):
        self.title = title
        self.items = _ItemsEndpoint(load)

        class _FieldsEndpoint:
            def get(self):
                return _Query(lambda _: fields, None)

        self.fields = _FieldsEndpoint()


class _TaxonomyError(Exception):
    """Duck-type of a ClientRequestException from an orphaned term set."""

    def __init__(self):
        super().__init__("The given guid does not exist in the term store")
        self.code = "-2146232832, Microsoft.SharePoint.SPFieldValidationException"
        self.message = "The given guid does not exist in the term store"


class _Opaque:
    """A SharePoint-entity-like value with no JSON representation."""

    def __str__(self):
        return "<opaque value>"


def test_export_and_verify_with_opaque_values(tmp_path):
    """Records with entity values still export, checksum, and verify cleanly."""
    loaded = [_Item(1, {"Id": 1, "Title": "hello", "Opaque": _Opaque()})]
    source = SharePointListSource(cast("SPList", _List("Docs", lambda _: loaded, [])))
    job = MigrationJob(source, JsonFileTarget(tmp_path / "out"))

    manifest = job.plan()
    assert len(manifest) == 1
    stats = job.run()
    assert stats.errors == 0

    assert (tmp_path / "out" / "1.json").exists()
    assert job.verify().ok


def _records(items) -> dict:
    return {item.id: item.properties for item in items}


def test_healthy_list_uses_full_read_without_warnings():
    loaded = [_Item(1, {"Id": 1, "Title": "a"}), _Item(2, {"Id": 2, "Title": "b"})]
    calls = []

    def load(select):
        calls.append(select)
        return loaded

    source = SharePointListSource(cast("SPList", _List("Docs", load, [])))
    result = source.list_items()

    assert len(result) == 2  # noqa: PLR2004
    assert calls == [None]  # full read, no select, no fallback
    assert source.warnings == []
    assert source.read(result[0]) == {"Id": 1, "Title": "a"}


def test_taxonomy_failure_falls_back_to_safe_select():
    selects = []

    def load(select):
        selects.append(select)
        if select is None:
            raise _TaxonomyError()
        return [_Item(1, {k: "" for k in select})]

    fields = [
        _Field("Id"),
        _Field("Title"),
        _Field("Topics", type_as_string="TaxonomyFieldType"),
        _Field("Tags", schema_xml='<Field ... TermSetId="1234-..."/>'),
        _Field("MainLinkSettings", hidden=True),  # restricted system column
    ]
    source = SharePointListSource(cast("SPList", _List("Docs", load, fields)))
    result = source.list_items()

    assert len(result) == 1
    assert any("excluded Managed Metadata" in w for w in source.warnings)
    fallback = selects[-1]
    assert "Topics" not in fallback and "Tags" not in fallback
    assert "MainLinkSettings" not in fallback  # hidden/system columns are not projected
    assert "Title" in fallback
    # records no longer materialize the orphaned taxonomy column
    assert "Topics" not in source.read(result[0])


def test_safe_read_denied_cascades_to_id_title_only():
    selects = []

    def load(select):
        selects.append(select)
        if select is None:
            raise _TaxonomyError()
        if len(select) > 2:  # noqa: PLR2004 — the visible-column read is denied too
            raise PermissionError("denied")
        return [_Item(1, {"Id": 1, "Title": "only"})]

    fields = [_Field("Id"), _Field("Title"), _Field("Notes")]
    source = SharePointListSource(cast("SPList", _List("Docs", load, fields)))
    result = source.list_items()

    assert len(result) == 1
    assert selects[-1] == ["Id", "Title"]
    assert any("denied too" in w for w in source.warnings)


def test_explicit_select_is_honored_and_not_silently_stripped():
    def load(select):
        raise _TaxonomyError()

    source = SharePointListSource(cast("SPList", _List("Docs", load, [])), select=["Id", "Topics"])
    try:
        source.list_items()
    except _TaxonomyError:
        pass
    else:
        raise AssertionError("expected the taxonomy failure to propagate when a select is given")
    assert source.warnings == []


def test_taxonomy_helpers():
    assert is_taxonomy_validation(_TaxonomyError())
    assert not is_taxonomy_validation(ValueError("boom"))

    fields = [
        _Field("Title"),
        _Field("Topics", type_as_string="TaxonomyFieldTypeMulti"),
    ]
    assert taxonomy_internal_names(fields) == ["Topics"]
    assert taxonomy_internal_names([_Field("Title")]) == []


def test_export_rerun_overwrites_and_verifies_clean(tmp_path):
    """Re-running an export into the same folder overwrites and still verifies."""

    loaded = [_Item(1, {"Id": 1, "Title": "hello"})]
    out = tmp_path / "out"

    def make():
        source = SharePointListSource(cast("SPList", _List("Docs", lambda _: loaded, [])))
        return MigrationJob(
            source,
            JsonFileTarget(out),
            options=MigrationOptions(conflict_resolution=ConflictResolution.OVERWRITE),
        )

    job = None
    for _ in range(2):  # noqa: PLR2004
        job = make()
        job.plan()
        stats = job.run()
        assert stats.success == 1 and stats.skipped == 0

    assert job is not None
    assert job.verify().ok


def test_assessor_flags_taxonomy_issue():
    source = type("Web", (), {"context": type("Ctx", (), {})()})()
    assessor = MigrationAssessor(cast("Web", source))
    report = AssessmentReport()

    assessor._flag_access(report, "/sites/x/web/lists/Announcements", _TaxonomyError())
    issue = report.issues[0]
    assert issue.severity == "warning"
    assert issue.category == "taxonomy"
    assert "term" in issue.message
    assert issue.suggestion  # actionable guidance

    # a non-taxonomy failure still gets the generic access warning
    report2 = AssessmentReport()
    assessor._flag_access(report2, "/sites/x/web/lists/Announcements", ValueError("denied"))
    assert report2.issues[0].category == "access"


if __name__ == "__main__":
    import sys

    import pytest

    sys.exit(pytest.main([__file__, "-v"]))


class _UrlItem:
    def __init__(self, url: str, length: int = 0):
        self.server_relative_url = url
        self.length = length


class _LibraryQuery:
    def __init__(self, result):
        self._result = result

    def execute_query(self):
        return self._result


class _FolderLibrary:
    """A library root whose ServerRelativeUrl is not loaded until requested."""

    def __init__(self, folders, files):
        self.server_relative_url = None
        self._folders = folders
        self._files = files

    def ensure_properties(self, _props):
        self.server_relative_url = "/sites/proj/Shared Documents"
        return _LibraryQuery(self)

    def get_folders(self, recursive=False):
        return _LibraryQuery(self._folders)

    def get_files(self, recursive=False):
        return _LibraryQuery(self._files)


def test_library_source_omits_site_and_library_prefix(tmp_path):
    from office365.migration.sharepoint.adapters import SharePointLibrarySource

    folder = _FolderLibrary(
        folders=[_UrlItem("/sites/proj/Shared Documents/Archive")],
        files=[_UrlItem("/sites/proj/Shared Documents/Forms/Document/1.txt", length=3)],
    )
    source = SharePointLibrarySource(cast("Folder", folder))
    items = source.list_items()

    dests = sorted(i.dest_path for i in items)
    assert dests == ["Archive/", "Forms/Document/1.txt"]  # no site/list prefix
    assert folder.server_relative_url == "/sites/proj/Shared Documents"  # root was loaded
