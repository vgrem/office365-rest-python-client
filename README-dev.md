# Installing to virtualenv

```bash
uv sync
```

## Running tests

Most of the tests are end-to-end - operations are invoked against actual tenant (not mocked).
So one has to configure his/her office/sharepoint credentials.
To do so, create a file ```.env``` like this (replace the bracketed values by your values):

```bash
export office365_python_sdk_securevars='{username};{password};{client_id};{client_secret}'
```

This file is in .gitignore, so it will never be committed.

```bash
. .env   # source it to export the variable
pytest ...  # run the test(s) you need...
```

## Configure Tenant

Roles:

- Global reader
- Groups admin
- Search admin
- SharePoint admin
- Teams service admin
- Users admin
