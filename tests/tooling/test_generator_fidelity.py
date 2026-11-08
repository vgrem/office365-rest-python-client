"""What the fidelity report answers, over a model small enough to have one of each.

The report is only as good as its reading of the source, and three readings are easy to
get wrong in ways that stay quiet: a name stated by ``name=`` keyword rather than
positionally, a member inherited from a class in another package (the subclass serves
it), and a class that states no type name at all (SharePoint derives it from the class
name). Each has a case here, and the gaps assertion pins what the report does *not*
count: a member the configured filters skip is reported, and is not a defect.
"""

from __future__ import annotations

from pathlib import Path

from generator.odata.model import ODataModel
from generator.odata.property import PropertyInformation
from generator.odata.type_information import TypeInformation
from generator.tools.fidelity import audit, gaps, read_models

_SOURCE = '''
from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.types.odata_property import odata


class Base:
    _odata_type_name = "Demo.Base"

    @odata(name="Inherited")
    @property
    def inherited(self): ...


class Thing(Base):
    _odata_type_name = "Demo.Thing"

    @odata(name="Title", beta=True)
    @property
    def title(self): ...

    @odata("Kept")
    @property
    def kept(self): ...

    @odata(name="Invented")
    @property
    def invented(self): ...

    @odata(name="Overseas")
    @property
    def overseas(self): ...

    Plain: Optional[str] = None


class Silent(Base):
    """States no name: SharePoint spells this one ``SP.Silent``."""

    Kept: Optional[str] = None
'''


def _metadata() -> ODataModel:
    """A base type and a derived one, between them one member of every kind."""
    return (
        ODataModel()
        .add_type(
            TypeInformation(
                FullName="Demo.Base",
                Properties={
                    "Inherited": PropertyInformation(Name="Inherited", TypeName="Edm.String", IsBeta=True),
                    "Dropped": PropertyInformation(Name="Dropped", TypeName="Edm.String"),
                    "Skipped": PropertyInformation(Name="Skipped", TypeName="Demo.Quiet"),
                },
            )
        )
        .add_type(
            TypeInformation(
                FullName="Demo.Thing",
                BaseTypeName="Demo.Base",
                Properties={
                    "Title": PropertyInformation(Name="Title", TypeName="Edm.String", IsBeta=True),
                    "Kept": PropertyInformation(Name="Kept", TypeName="Edm.String"),
                    "Plain": PropertyInformation(Name="Plain", TypeName="Edm.String"),
                    "Novel": PropertyInformation(Name="Novel", TypeName="Edm.String", IsBeta=True),
                    "Overseas": PropertyInformation(Name="Overseas", TypeName="Edm.String", ReadOnly=True),
                },
            )
        )
    )


def _package(tmp_path: Path, prefix: str = "") -> Path:
    package = tmp_path / "demo"
    package.mkdir(exist_ok=True)
    (package / "thing.py").write_text(_SOURCE, encoding="utf-8")
    return package


def test_the_report_names_every_way_a_model_can_disagree_with_the_metadata(tmp_path: Path) -> None:
    findings = audit(
        read_models(_package(tmp_path)),
        _metadata(),
        ignored_types=["Demo.Quiet"],
        ignored_properties=["Dropped"],
    )

    assert {(finding.kind, finding.member) for finding in findings} == {
        ("beta", "Inherited"),  # inherited, and so still the subclass's to declare
        ("undeclared", "Plain"),  # a field that serializes under its own spelling
        ("missing", "Novel"),  # a column the model does not state at all
        ("extra", "Invented"),  # a member the metadata does not declare
        ("readonly", "Overseas"),
        ("ignored", "Dropped"),  # an ``ignored_properties`` entry
        ("ignored", "Skipped"),  # a column typed as an ``ignored_types`` name
    }


def test_a_skip_the_configuration_asks_for_is_not_a_gap(tmp_path: Path) -> None:
    findings = audit(
        read_models(_package(tmp_path)),
        _metadata(),
        ignored_types=["Demo.Quiet"],
        ignored_properties=["Dropped"],
    )

    assert {finding.member for finding in gaps(findings)} == {"Inherited", "Plain", "Novel", "Overseas", "Invented"}


def test_a_class_that_states_no_type_name_is_named_the_way_the_service_names_it(tmp_path: Path) -> None:
    models = {model.name: model for model in read_models(_package(tmp_path), "SP")}

    assert models["Thing"].type_name == "Demo.Thing"
    assert models["Silent"].type_name == "SP.Silent"
    assert "Inherited" in models["Silent"].members  # the ancestor's member is the subclass's
    assert not models["Silent"].members["Kept"].declared
