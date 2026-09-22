"""Unified access to service limits — mechanics, catalogs and discovery.

The library declares limits in three layers:

- **Mechanics** (:mod:`office365.runtime.limits`): :class:`Limit` (a static
  threshold *or* a rate quota), the :func:`limit` decorator, and the guardrails
  (:func:`exceeds` / :func:`warn_if_exceeds` / :func:`ensure_within` /
  :func:`hint`).
- **Catalogs**: product vocabularies — e.g. ``sharepoint.thresholds.Limits``
  (SharePoint) and the model-bound Graph quotas (``directory.quotas`` /
  ``communications.quotas``).
- **Discovery**: a class carries its limits via ``@limit`` (``declared_limits()``);
  :func:`limits_of` / :func:`verify_limits` inspect them; :func:`catalog`
  aggregates every registered source.

Products register their catalogs with :func:`register_catalog`; ``@limit`` on a
class registers that class automatically (under ``product="model"``).
"""

from __future__ import annotations

from office365.runtime.limits import (
    DEFAULT_BATCH_SIZE,
    SAFE_PAGE_SIZE,
    Limit,
    LimitCatalog,
    LimitDecl,
    LimitExceededError,
    LimitKind,
    LimitReport,
    bounded,
    catalog,
    collect_class_limits,
    collect_limit_meta,
    ensure_within,
    exceeds,
    hint,
    limit,
    limits_of,
    register_catalog,
    verify_limits,
    warn_if_exceeds,
)

__all__ = [
    "DEFAULT_BATCH_SIZE",
    "SAFE_PAGE_SIZE",
    "Limit",
    "LimitCatalog",
    "LimitDecl",
    "LimitExceededError",
    "LimitKind",
    "LimitReport",
    "bounded",
    "catalog",
    "collect_class_limits",
    "collect_limit_meta",
    "ensure_within",
    "exceeds",
    "hint",
    "limit",
    "limits_of",
    "register_catalog",
    "verify_limits",
    "warn_if_exceeds",
]
