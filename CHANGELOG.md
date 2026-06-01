# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

- (placeholder for upcoming changes)

## [3.0.0]

### Breaking
- **Python 2 dropped** — minimum Python version is now 3.8
- **ACS/SAML retirement** — `with_user_credentials` now raises `RuntimeError` for SharePoint Online. Use `with_username_and_password` (MSAL ROPC) instead. ACS App-Only (`with_client_credentials`) marked as deprecated.
- **USGovernment GCC endpoints corrected** — were using wrong URLs

### Added
- Full type hints across all modules (runtime, directory, onedrive, outlook, teams, sharepoint, intune, and more)
- `with_username_and_password` (MSAL ROPC) for SharePoint Online auth

### Fixed
- Cryptography CVEs updated to 48.0.0
- Circular import in `client_runtime_context.py` / `read_entity.py`
- `NameError: name 'List' is not defined` in `fields/collection.py`
- `single()` and `first()` return types (never return `None`)

### Removed
- Python 2.7 support
- `.travis.yml` (use GitHub Actions instead)
- `requirements.txt` / `requirements-dev.txt` (use `uv`/`pyproject.toml`)

---

## [2.6.2]

- Support Access Token Refresh for MSAL-provided tokens ([#953](https://github.com/vgrem/office365-rest-python-client/issues/953))
- Resolved `get_comments()` method issue ([#956](https://github.com/vgrem/office365-rest-python-client/issues/956))
- Added Reply-To and HTML ItemBody type support in `send_mail` ([#958](https://github.com/vgrem/office365-rest-python-client/issues/958))
- Fixed `File.open_binary` issue ([#960](https://github.com/vgrem/office365-rest-python-client/issues/960))
- Fixed linting GitHub Action ([#961](https://github.com/vgrem/office365-rest-python-client/issues/961))

## [2.6.0]

- Support for Azure environments in `ClientContext` (USGovernment, GCC High, etc.)
- Auto-renewal of authentication cookies for `with_user_credentials` (after 30 min expiry) ([#950](https://github.com/vgrem/office365-rest-python-client/issues/950))
- Support for worksheet [used range](https://learn.microsoft.com/en-us/graph/api/worksheet-usedrange) API ([#926](https://github.com/vgrem/office365-rest-python-client/issues/926))

## [2.5.14]

- Added `include_resource_data` to `SubscriptionCollection.add` ([#900](https://github.com/vgrem/office365-rest-python-client/issues/900), [#901](https://github.com/vgrem/office365-rest-python-client/issues/901))
- Added urllib percent-encoding to URLs ([#918](https://github.com/vgrem/office365-rest-python-client/issues/918))
- Microsoft Search API enhancements

## [2.5.13]

- JSON batch request fixes ([#835](https://github.com/vgrem/office365-rest-python-client/issues/835))

## [2.5.12]

- Batch request fixes and improvements ([#788](https://github.com/vgrem/office365-rest-python-client/issues/788))

## [2.5.11]

- Fixed error creating a choice field ([#873](https://github.com/vgrem/office365-rest-python-client/issues/873))
- Fixed `shares.by_url` method ([#872](https://github.com/vgrem/office365-rest-python-client/issues/872))
- Fixed failing driveItem move operation ([#627](https://github.com/vgrem/office365-rest-python-client/issues/627))
- Bumped MSAL dependency ([#869](https://github.com/vgrem/office365-rest-python-client/issues/869))

## [2.5.10]

- Fixed path issue when addressing drive items ([#866](https://github.com/vgrem/office365-rest-python-client/issues/866))

## [2.5.9]

- `DriveItem.get_files` and `get_folders` now retrieve all items beyond default page size ([#844](https://github.com/vgrem/office365-rest-python-client/issues/844))
- Fixed `__str__` raising exception when `DecodeUrl` is `None` ([#850](https://github.com/vgrem/office365-rest-python-client/issues/850))
- Added note for Entra ID permissions when updating SP metadata fields ([#847](https://github.com/vgrem/office365-rest-python-client/issues/847))

## [2.5.8]

- SharePoint resource addressing enhancements
- Introduced methods for granting and revoking delegated & application permissions

## [2.5.7]

- Added passphrase support in `ClientContext.with_client_certificate` ([#836](https://github.com/vgrem/office365-rest-python-client/issues/836))

## [2.5.6]

- Support for folder coloring in SharePoint API ([#693](https://github.com/vgrem/office365-rest-python-client/issues/693))

## [2.5.5]

- Better Range support in OneDrive API ([#745](https://github.com/vgrem/office365-rest-python-client/issues/745))

## [2.5.4]

- SharePoint authentication support for GCC High environments ([#794](https://github.com/vgrem/office365-rest-python-client/issues/794))
- Fixed listing folders instead of files ([#802](https://github.com/vgrem/office365-rest-python-client/issues/802))
- Fixed addressing shared drive items ([#801](https://github.com/vgrem/office365-rest-python-client/issues/801))

## [2.5.3]

- Added `file_name` parameter to `File.copyto` and `File.copyto_using_path` ([#787](https://github.com/vgrem/office365-rest-python-client/issues/787))
- Fixed import error for `TypedDict` on Python 3.7 ([#781](https://github.com/vgrem/office365-rest-python-client/issues/781))
- Fixed `parent_folder` / `parent_collection` empty when retrieving file by server-relative URL ([#764](https://github.com/vgrem/office365-rest-python-client/issues/764))
- Fixed 401 on site property update ([#735](https://github.com/vgrem/office365-rest-python-client/issues/735))
- Fixed recipient instance reuse ([#791](https://github.com/vgrem/office365-rest-python-client/issues/791))

## [2.5.2]

- Fixed missing `typing_extensions` dependency on older Python ([#762](https://github.com/vgrem/office365-rest-python-client/issues/762))
- File/folder addressing methods fixes ([#764](https://github.com/vgrem/office365-rest-python-client/issues/764))
- Fixed share file with password ([#766](https://github.com/vgrem/office365-rest-python-client/issues/766))
- Fixed change token entity type name ([#767](https://github.com/vgrem/office365-rest-python-client/issues/767))
- Documentation fixes ([#768](https://github.com/vgrem/office365-rest-python-client/issues/768))
- CI/Linting improvements ([#765](https://github.com/vgrem/office365-rest-python-client/issues/765))

## [2.5.1]

- Added conditional import of `ParamSpec` from `typing_extensions` ([#757](https://github.com/vgrem/office365-rest-python-client/issues/757))

## [2.5.0]

- Introduced `GraphClient.with_client_secret` and `GraphClient.with_username_and_password`
- Fixed `Folder.copy_to_using_path` ([#740](https://github.com/vgrem/office365-rest-python-client/issues/740))
- Fixed `File.download_session` ([#748](https://github.com/vgrem/office365-rest-python-client/issues/748))
- Fixed `ResourcePath` collection ([#744](https://github.com/vgrem/office365-rest-python-client/issues/744))
- Typing improvements (mypy/pyright support) ([#746](https://github.com/vgrem/office365-rest-python-client/issues/746), [#747](https://github.com/vgrem/office365-rest-python-client/issues/747))

## [2.4.4]

- Fixed `FieldCollection.add_dependent_lookup_field` ([#723](https://github.com/vgrem/office365-rest-python-client/issues/723))
- Fixed 404 error with `Web.get_file_by_server_relative_path` ([#722](https://github.com/vgrem/office365-rest-python-client/issues/722))

## [2.4.3]

- Support for interactive auth via `ClientContext.with_interactive`
- Support for OAuth2 device code auth ([#713](https://github.com/vgrem/office365-rest-python-client/issues/713))
- Fixed bug with losing event handlers ([#682](https://github.com/vgrem/office365-rest-python-client/issues/682))

## [2.4.2]

- Fixed error when file is addressed by path ([#645](https://github.com/vgrem/office365-rest-python-client/issues/645))
- File/folder addressing now supports site-relative and web-relative URLs
- Support for long-running actions in Teams API with polling status
