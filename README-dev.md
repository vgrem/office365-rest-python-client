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

Most tests are end-to-end and run against a real tenant. Configure your credentials in a `.env` file:

```bash
export office365_python_sdk_securevars='{username};{password};{client_id};{client_password}'
```

This file is `.gitignore`d. Source it before running tests:

```bash
$ . .env
$ pytest                        # all tests
$ pytest tests/test_sharepoint   # specific area
```

### Required tenant roles

The test account needs these [Azure AD roles](https://learn.microsoft.com/en-us/azure/active-directory/roles/permissions-reference) assigned:

- Global reader
- Groups admin
- Search admin
- SharePoint admin
- Teams service admin
- Users admin
