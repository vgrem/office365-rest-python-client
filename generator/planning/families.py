"""Families a product's tree already keeps in a folder of their own.

:func:`~generator.planning.routing.descend_module` descends by **word prefix**: a new
``VivaAuditRecord`` becomes ``audit/viva_record.py``, because ``viva`` is the first word.
That is right for a folder named after the type's opening word and wrong for a *family*:
the tree keeps every ``*AuditRecord`` under ``audit/records``, and the source word is the
subfolder inside it, not the stem.

So the families are a table, and they answer before the word prefix does:

* the **folder** says the family, so the stem drops the family word
  (``ai_agent_evidence.py`` -> ``evidence/ai_agent.py``);
* a family with ``by_source`` descends one level further into a *sub*folder named after
  the type's leading word when that folder exists (``audit/records/viva``), and drops
  the word from the stem because the folder repeats it;
* a folder that does not exist is never created: an unknown source word keeps its full
  stem inside the family folder (``audit/records/fabric_audit_record.py``), and the move
  into a real folder later is allowed to shorten it.

A family names the **subtree** it governs, not the whole product: ``*AuditRecord`` is
claimed anywhere under ``office365.security.audit``, ``*Evidence`` anywhere under
``office365.security.alerts``. The line matters -- a product-wide ``*Status`` rule would
drag ``SimulationStatus`` out of ``attacksimulations/`` and into an alert folder that
never reads it.
"""

from __future__ import annotations

import ast
import os
from dataclasses import dataclass

from generator.build.naming import to_snake_case


@dataclass(frozen=True)
class Family:
    """One family of types that a package keeps in a folder of its own."""

    #: Module subtree the family governs; the rule applies to it and below.
    scope: str
    #: Every class name ending with this belongs to the family.
    suffix: str
    #: Folder inside ``office365``, slash-separated: ``security/audit/records``.
    folder: str
    #: Descend into ``<folder>/<leading word>`` when that folder exists.
    by_source: bool = False


#: Longest suffix wins, so ``ObjectIdAction`` beats ``Action``.
FAMILIES: tuple[Family, ...] = (
    Family("office365.security.audit", "AuditRecord", "security/audit/records", by_source=True),
    Family("office365.security.alerts", "Evidence", "security/alerts/evidence"),
    Family("office365.security.alerts", "EntityMapping", "security/alerts/entitymappings"),
    Family("office365.security.alerts", "ObjectIdAction", "security/alerts/actions"),
    Family("office365.security.alerts", "State", "security/alerts/states"),
    Family("office365.security.alerts", "Status", "security/alerts/states"),
)


def _module_of(folder: str) -> str:
    """``security/audit/records`` -> ``office365.security.audit.records``."""
    return "office365." + folder.strip("/").replace("/", ".")


def _defines_class(path: str, class_name: str) -> bool:
    try:
        with open(path, encoding="utf-8") as f:
            tree = ast.parse(f.read())
    except (OSError, SyntaxError):
        return False
    return any(isinstance(node, ast.ClassDef) and node.name == class_name for node in tree.body)


def _free(directory: str, stem: str, class_name: str) -> bool:
    """Whether ``<directory>/<stem>.py`` is absent or holds the same class."""
    path = os.path.join(directory, stem + ".py")
    return not os.path.isfile(path) or _defines_class(path, class_name)


def family_target(package: str, class_name: str, output_base: str) -> tuple[str, str] | None:
    """The folder module and stem a family claims for ``class_name``, or ``None``.

    ``None`` means no family answers, and the word-prefix descent should run instead.
    """
    if not output_base:
        return None
    for family in sorted(FAMILIES, key=lambda item: len(item.suffix), reverse=True):
        if class_name.endswith(family.suffix) and (package == family.scope or package.startswith(family.scope + ".")):
            break
    else:
        return None
    directory = os.path.join(output_base, *family.folder.split("/"))
    if not os.path.isdir(directory):
        return None
    stem = to_snake_case(class_name, avoid_keywords=False)
    if family.by_source:
        word, _, trimmed = stem.partition("_")
        source = os.path.join(directory, word)
        if trimmed and os.path.isdir(source) and _free(source, trimmed, class_name):
            return _module_of(f"{family.folder}/{word}"), trimmed
    suffix = to_snake_case(family.suffix, avoid_keywords=False)
    if not family.by_source and stem.endswith("_" + suffix):
        trimmed = stem[: -len(suffix) - 1]
        if _free(directory, trimmed, class_name):
            return _module_of(family.folder), trimmed
    return _module_of(family.folder), stem


__all__ = ["FAMILIES", "Family", "family_target"]
