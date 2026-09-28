# Installation

`office365-rest-python-client` supports Python 3.8+ and has a single runtime
dependency: [`requests`](https://requests.readthedocs.io/).

## From PyPI

```bash
pip install office365-rest-python-client
```

## With uv

```bash
uv pip install office365-rest-python-client
```

## Latest from GitHub

Unreleased changes are on `master` — install straight from the repo:

```bash
pip install git+https://github.com/vgrem/office365-rest-python-client.git
```

## Upgrading

```bash
pip install --upgrade office365-rest-python-client
```

## Optional extras

Features that need a third-party package are extras:

```bash
pip install "office365-rest-python-client[httpx]"     # native-async HTTP transport
pip install "office365-rest-python-client[pandas]"    # DataFrames
pip install "office365-rest-python-client[excel]"     # Excel
pip install "office365-rest-python-client[parquet]"   # Parquet
pip install "office365-rest-python-client[sql]"       # SQLAlchemy
pip install "office365-rest-python-client[duckdb]"    # DuckDB
```

---

Once installed, head to **[Getting Started](getting-started.md)** to pick your
client and make your first call.
