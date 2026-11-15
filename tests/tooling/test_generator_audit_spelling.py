"""A type the wire spells in camelCase is measured, not skipped.

One type has two spellings. The model index Pascal-cases the last segment of a CSDL name
(``listItem`` reads as ``ListItem``) because that is the class it generates, while
``entity_type_name`` answers with the name the wire uses. Matched on the exact string,
the pair looked like a type the snapshot does not declare at all: no row, no finding, and
a clean report that meant "not measured". The audit resolves a model's name through the
snapshot's own names, so both spellings reach the same row.

The two cases below are what that resolution buys: a member the class holds but does not
declare becomes visible, and a base type the metadata names becomes nameable. The debt
they expose is carried in ``generator/audit-baseline.json``.

The whole tree is read once for both, as the CLI does it: a base type is named only when
the subtree holding it is in scope, and ``security.Artifact`` lives outside the package
that spells it.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import List

from generator.cli.session import Session
from generator.tools.fidelity import BASE, UNDECLARED, Finding, audit, read_models


@lru_cache(maxsize=1)
def _findings() -> List[Finding]:
    session = Session.open("graph")
    model_root = Path(session.options.output_path).resolve()
    return audit(read_models(model_root, "", model_root), session.read_model())


def _in(package: str) -> List[Finding]:
    return [finding for finding in _findings() if f"/{package}/" in finding.path]


def test_a_camel_case_type_is_measured_rather_than_passing_as_unmeasured() -> None:
    findings = [finding for finding in _in("todo") if finding.type_name == "microsoft.graph.attachmentInfo"]

    assert {finding.kind for finding in findings} == {UNDECLARED}
    assert {finding.member for finding in findings} == {"attachmentType", "contentType", "name", "size"}


def test_a_camel_case_base_is_named_as_the_base_the_subclass_lacks() -> None:
    findings = [finding for finding in _in("security/threatintelligence") if finding.kind == BASE]

    assert {finding.model for finding in findings} >= {"Host", "HostComponent", "HostCookie"}
    assert {finding.member for finding in findings} == {"Artifact"}
