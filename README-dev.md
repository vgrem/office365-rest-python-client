# Prerequisites

- Python >= 3.8
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

# Setup

## With uv (recommended)

```bash
$ uv venv
$ source .venv/bin/activate
$ uv sync
```

## With pip

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -e ".[examples,ntlm]"
```

## Running tests

Most tests are end-to-end and run against a real tenant. Configure your credentials in a `.env` file in the project root:

```bash
OFFICE365_TENANT=contoso.onmicrosoft.com
OFFICE365_CLIENT_ID=00000000-0000-0000-0000-000000000000
OFFICE365_CLIENT_SECRET=...
OFFICE365_USERNAME=admin@contoso.onmicrosoft.com
OFFICE365_PASSWORD=...
```

This file is `.gitignore`d — `tests/settings.py` reads it automatically, so just run:

```bash
$ pytest                        # all tests
$ pytest tests/sharepoint       # specific area
```

### Required tenant roles

The test account needs these [Azure AD roles](https://learn.microsoft.com/en-us/azure/active-directory/roles/permissions-reference) assigned:

- Global reader
- Groups admin
- Search admin
- SharePoint admin
- Teams service admin
- Users admin
