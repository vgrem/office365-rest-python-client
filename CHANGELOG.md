# Changelog

## 3.0.0 — 2026-05-18

### Major Changes

- **Python 2 dropped** — minimum Python version is now 3.8.
  The codebase is fully Python 3 native with no compatibility shims.
- **ACS/SAML retirement** — `with_user_credentials` now raises a clear
  `RuntimeError` for SharePoint Online. Use `with_username_and_password` (MSAL ROPC) instead.
  ACS App-Only (`with_client_credentials`) marked as deprecated with retirement notice.
- **Pyright type checking** — the entire `office365/` package is now in scope
  with **0 type errors**.
- **Ruff linting** — all rules enabled except 2 justified ignores (B008, PLC0415).

### Added

- Full type hints across all modules (runtime, directory, onedrive, outlook, teams,
  booking, sharepoint, intune, and more).
- Expanded pyright scope from 4 directories to the entire `office365/` package.
- Generator templates now emit `from __future__ import annotations`.
- CHANGELOG.md (this file).

### Fixed

- 237+ pyright type errors resolved during scoping.
- Circular import in `client_runtime_context.py` / `read_entity.py`.
- `NameError: name 'List' is not defined` in `fields/collection.py` at runtime.
- `single()` and `first()` return types corrected (never return `None`).
- `after_execute` callback type corrected (was claiming `Self`, actually receives `Any`).
- Cryptography CVE-2026-26007, CVE-2026-39892, CVE-2026-34073 fixed (updated to 48.0.0).
- Removed unused `astunparse` dependency (removed transitive `wheel` CVE).
- Moved `pyright` from runtime to dev dependencies.
- USGovernment GCC endpoints corrected (were using wrong URLs).
- TypeVars renamed for clarity (`T` → `ClientObjectT`, `ReturnT`, `ValueT`, `FuncT`).

### Changed

- **README restructured** — organized by client (ClientContext vs GraphClient),
  auth section split by modern/legacy with ACS retirement banner.
- **Auth examples reorganized** into `modern/` and `legacy/` subdirectories.
- **Generator templates** now include `from __future__ import annotations`.
- Ruff config cleaned — removed 10 unused ignore rules.
- `.travis.yml` removed (dead CI config with hardcoded credentials).

### Removed

- Python 2.7 support.
- `.travis.yml` (use GitHub Actions instead).
- `requirements.txt` / `requirements-dev.txt` (use `uv` / `pyproject.toml`).
- Unused `astunparse` dev dependency.
- `pyright` runtime dependency (now dev-only).
