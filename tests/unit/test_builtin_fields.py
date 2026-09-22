"""Tests for the canonical built-in SharePoint field names/ids."""

from __future__ import annotations

from office365.migration.sharepoint import SharePointAssessmentOptions
from office365.sharepoint.fields.builtin_field_id import SPBuiltInFieldId
from office365.sharepoint.fields.builtin_field_name import (
    EXTRA_SYSTEM_FIELD_NAMES,
    SYSTEM_FIELD_NAMES,
    SPBuiltInFieldName,
)


def test_builtin_field_name_lookup():
    assert SPBuiltInFieldName.FileLeafRef == "FileLeafRef"
    assert SPBuiltInFieldName.FSObjType == "FSObjType"
    assert SPBuiltInFieldName.is_builtin("ContentTypeId")
    assert not SPBuiltInFieldName.is_builtin("MyColumn")


def test_system_field_names_include_extras():
    assert SPBuiltInFieldName.ALL <= SYSTEM_FIELD_NAMES
    assert "AppAuthor" in EXTRA_SYSTEM_FIELD_NAMES
    assert "AppAuthor" in SYSTEM_FIELD_NAMES
    assert "MyColumn" not in SYSTEM_FIELD_NAMES


def test_assessment_options_default_from_canonical_set():
    assert SharePointAssessmentOptions().system_field_names == set(SYSTEM_FIELD_NAMES)


def test_builtin_field_id_guids():
    assert SPBuiltInFieldId.FileLeafRef == "{8553196d-ec8d-4564-9861-3dbe931050c8}"
    assert SPBuiltInFieldId.Author == "{1df5e554-ec7e-46a6-901d-d85a3881cb18}"
    assert SPBuiltInFieldId.ID.startswith("{") and SPBuiltInFieldId.ID.endswith("}")
