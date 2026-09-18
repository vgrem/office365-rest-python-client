"""SQL/DuckDB record streaming — the optional-dependency boundary.

``from_sql``/``from_duckdb`` accept a connection object (SQLAlchemy
``Engine``/``Connection``, DuckDB connection) or a connection string, plus a
query, and yield record batches (bounded memory). ``to_sql``/``to_duckdb`` write
loaded records to a table. Dependencies are imported lazily:
``[sql]`` (SQLAlchemy) and ``[duckdb]``.
"""

from __future__ import annotations

from typing import Any, Dict, Iterator, List


def require_sqlalchemy():
    """Import SQLAlchemy or raise an actionable error."""
    try:
        import sqlalchemy  # type: ignore[import-not-found]
    except ImportError:
        raise ImportError("pip install office365-rest-python-client[sql]") from None
    return sqlalchemy


def sql_chunks(source: Any, query: str, chunksize: int) -> Iterator[List[Dict[str, Any]]]:
    """Yield record batches from a SQLAlchemy engine/connection (or URL string)."""
    from office365.runtime.converters.dataframe import require_pandas

    engine = source
    if isinstance(source, str):
        engine = require_sqlalchemy().create_engine(source)
    for chunk in require_pandas().read_sql_query(query, engine, chunksize=chunksize):
        yield chunk.to_dict("records")


def write_sql(records: List[Dict[str, Any]], target: Any, *, table: str, **opts: Any) -> None:
    """Write records to a SQL table (SQLAlchemy connection/engine or URL)."""
    from office365.runtime.converters.dataframe import require_pandas

    engine = target
    if isinstance(target, str):
        engine = require_sqlalchemy().create_engine(target)
    require_pandas().DataFrame.from_records(records).to_sql(table, engine, **opts)


def duckdb_chunks(source: Any, query: str, chunksize: int) -> Iterator[List[Dict[str, Any]]]:
    """Yield record batches from a DuckDB connection (or database path)."""
    import duckdb  # type: ignore[import-not-found]

    connection = source if hasattr(source, "execute") else duckdb.connect(source)
    result = connection.execute(query)
    columns = [description[0] for description in result.description]
    while True:
        rows = result.fetchmany(chunksize)
        if not rows:
            break
        yield [dict(zip(columns, row)) for row in rows]


def write_duckdb(records: List[Dict[str, Any]], target: Any, *, table: str, **opts: Any) -> None:
    """Write records to a DuckDB table (connection or database path)."""
    import duckdb  # type: ignore[import-not-found]

    from office365.runtime.converters.dataframe import require_pandas

    connection = target if hasattr(target, "execute") else duckdb.connect(target)
    df = require_pandas().DataFrame.from_records(records)
    connection.register("_records_df", df)
    connection.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM _records_df")
    connection.unregister("_records_df")
