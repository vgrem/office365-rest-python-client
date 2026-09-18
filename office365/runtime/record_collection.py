"""A collection that can be exported to / imported from tabular and record formats.

Keeps the data-interchange concern (pandas/CSV/JSON/NDJSON/Excel) out of the core
:class:`~office365.runtime.client_object_collection.ClientObjectCollection`, and
exposes named conveniences (``to_csv``/``from_dataframe``/``queue_dataframe`` …)
and unified ``export_to``/``from_records`` entry points backed by a format
registry. ``from_*`` is the **streaming** entry (returns an
:class:`~office365.runtime.imports.ImportResult` driver — bounded, resumable,
idempotent); ``queue_*`` is the deferred queue-all entry.

Keyed imports (skip/upsert) are opt-in: a subclass exposes an
:class:`~office365.runtime.converters.upsert.UpsertTarget` via :meth:`upsert_target`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from os import PathLike
from typing import IO, TYPE_CHECKING, Any, Callable, Dict, Iterable, List, Optional, Union

from typing_extensions import Self

from office365.runtime.client_object import ClientObjectT
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.converters import registry

if TYPE_CHECKING:
    from office365.runtime.converters.dataframe import DataFrameResult
    from office365.runtime.converters.upsert import UpsertTarget
    from office365.runtime.imports import CheckpointStore, ImportCheckpoint, ImportResult
    from office365.runtime.operations import ProgressCallback


@dataclass
class VerificationResult:
    """Outcome of a key reconciliation (:meth:`RecordCollection.verify_keys`)."""

    checked: int = 0
    missing: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """Whether every checked key is present on the target."""
        return not self.missing

    def summary(self) -> str:
        status = "OK" if self.ok else "MISMATCH"
        return f"{status} | checked: {self.checked}, missing: {len(self.missing)}"


def _apply_mapping(convert: Callable[[Any], list[dict]], mapping: Dict[str, str]) -> Callable[[Any], list[dict]]:
    """Wrap a chunk converter to rename record keys (``source -> target``)."""

    def mapped(chunk: Any) -> list[dict]:
        return [{mapping.get(k, k): v for k, v in record.items()} for record in convert(chunk)]

    return mapped


class RecordCollection(ClientObjectCollection[ClientObjectT]):
    """A collection with record import/export capabilities."""

    # ── Export ───────────────────────────────────────────────────

    def export_to(self, target: Any, *, format: str = "csv", **opts: Any) -> Self:  # noqa: A002
        """Deferred export of the loaded items to ``target`` in ``format``.

        The writer is resolved from the format registry, so formats are pluggable.
        Run it with ``execute_query()``:

            >>> client.users.get_all().export_to(f, format="csv").execute_query()
        """
        writer = registry.writer_for(format)
        return self.after_execute(lambda _: writer(self, target, **opts))

    def to_records(self, raw: bool = False) -> List[Dict[str, Any]]:
        """Project loaded items into plain dict records — the neutral export form.

        The projection shared by every exporter: ``.select()``/``.expand()``
        columns, one record per expanded child item, native JSON-safe values.
        Unlike ``to_csv`` this returns a value directly, so load first.

        Args:
            raw: When True, keep native property values (no JSON coercion).
        """
        from office365.runtime.converters.records import iter_records

        return iter_records(self, raw=raw)

    def to_csv(self, file: IO[str]) -> Self:
        """Export loaded items to CSV (deferred)."""
        return self.export_to(file, format="csv")

    def to_ndjson(self, file: IO[str]) -> Self:
        """Export loaded items as NDJSON — one record per line (deferred)."""
        return self.export_to(file, format="ndjson")

    def to_excel(self, target: Union[str, PathLike]) -> Self:
        """Export loaded items to an Excel (.xlsx) worksheet (deferred).

        Requires the optional dependency (``pip install
        office365-rest-python-client[excel]``).
        """
        return self.export_to(target, format="excel")

    def to_dataframe(self) -> "DataFrameResult":
        """Build a pandas DataFrame from the loaded items (deferred result).

        Returns a ``DataFrameResult`` whose ``.value`` holds the DataFrame after
        ``execute_query()``. Requires the ``[pandas]`` extra.
        """
        from office365.runtime.converters.dataframe import DataFrameResult, require_pandas, write_dataframe

        require_pandas()  # fail fast on a missing optional dependency
        result = DataFrameResult(self.context)
        self.after_execute(lambda _: write_dataframe(self, result))
        return result

    # ── Import: deferred (queue-all) ─────────────────────────────

    def queue_records(self, records: List[dict], progress: "ProgressCallback | None" = None) -> Self:
        """Queue a create per record (deferred, run with ``execute_query()``).

        The neutral queue-all counterpart of :meth:`to_records`. Records are
        normalized to the item type and each becomes an entity queued for
        creation. Use the streaming :meth:`from_records` for large or
        resumable/idempotent imports (bounded memory).
        """
        from office365.runtime.converters.csv_reader import coerce_records

        return self._import_records(coerce_records(self._item_type, records), progress=progress)

    def queue_dataframe(self, df, progress: "ProgressCallback | None" = None) -> Self:
        """Queue a create per DataFrame row (deferred, run with ``execute_query()``)."""
        return self.queue_records(registry.reader_for("dataframe")(df), progress=progress)

    def _import_records(self, records: List[dict], progress: "ProgressCallback | None" = None) -> Self:
        """Queue a create per record, appending the pending entities to this collection."""
        from office365.runtime.operations import query_progress_hook
        from office365.runtime.queries.create_entity import CreateEntityQuery

        hook = query_progress_hook(len(records), progress) if callable(progress) else None
        for record in records:
            entity = self.create_typed_object(record)
            self.add_child(entity)
            qry = CreateEntityQuery(self, entity, entity)
            self.context.add_query(qry)
            if hook is not None:
                self.context.after_execute(hook)
        return self

    # ── Import: streaming (bounded, resumable, idempotent) ───────

    def from_records(
        self,
        source: Any,
        *,
        format: str = "records",  # noqa: A002
        chunksize: int = 2000,
        key: "str | list[str] | None" = None,
        key_field: str = "MigrationKey",
        on_conflict: str = "skip",
        enforce_unique: bool = False,
        checkpoint: "ImportCheckpoint | CheckpointStore | str | PathLike | None" = None,
        on_error: str = "raise",
        progress: "ProgressCallback | None" = None,
        prepare: "Callable[[Any], None] | None" = None,
        before_chunk: "Callable[[Any], None] | None" = None,
        to_records: "Callable[[Any], list[dict]] | None" = None,
        total: Optional[int] = None,
        dry_run: bool = False,
        dead_letter: "str | PathLike | None" = None,
        mapping: "Dict[str, str] | None" = None,
        coerce: "Dict[str, Callable[[Any], Any]] | None" = None,
    ) -> "ImportResult":
        """Stream a source into this collection, memory-bounded (the streaming entry).

        ``source`` is chunked by ``format``: ``dataframe``/``csv`` (a DataFrame,
        chunk iterable, or CSV path/URL/file), ``records`` (an iterable of record
        batches), or any registered format (read whole). Returns an
        :class:`~office365.runtime.imports.ImportResult`; choose the terminal
        (``execute_query``/``execute_batch``) or iterate it. ``key`` enables
        idempotent skip/upsert via :meth:`upsert_target`; ``mapping`` renames
        source columns/keys; ``coerce`` maps a record key to a value converter
        (used for typed destination fields).
        """
        from office365.runtime.imports import ImportResult

        chunks, convert, inferred_total = self._resolve_source(source, format, chunksize, to_records)
        if total is None:
            total = inferred_total
        if mapping:
            convert = _apply_mapping(convert, mapping)

        raw_key_columns = [key] if isinstance(key, str) else (list(key) if key else [])
        key_columns = [self._key_column(c) for c in raw_key_columns]
        target = self.upsert_target(key_field=key_field, enforce_unique=enforce_unique) if key_columns else None
        if key_columns and target is None:
            raise ValueError("key= requires an upsert-capable collection (override upsert_target())")
        existing: Dict[str, Any] = {}
        keys_loaded = False

        def _prepare(first_chunk: Any) -> None:
            if callable(prepare):
                prepare(first_chunk)

        def _ensure_keys() -> None:
            """Ensure the key column and load existing keys (once, on every run).

            Loading is lazy (on the first queued chunk) rather than part of the
            fresh-run-only ``prepare`` so a **resumed** run still skips records
            that are already present — the key load is what makes a replayed or
            overlapping chunk idempotent, not just a fresh run.
            """
            nonlocal keys_loaded
            if target is None or keys_loaded:
                return
            target.ensure_key_field()
            self.context.execute_query()
            existing.update(target.load_keys())
            keys_loaded = True

        def _queue(records: list[dict]) -> tuple[int, int]:
            if coerce:
                records = [
                    {
                        key: (coerce[key](value) if key in coerce and value is not None else value)
                        for key, value in record.items()
                    }
                    for record in records
                ]
            if target is None:
                if not dry_run:
                    self.queue_records(records)
                return len(records), 0
            from office365.runtime.converters.upsert import keyed_queue

            _ensure_keys()
            return keyed_queue(
                target,
                records,
                key_columns=key_columns,
                existing=existing,
                on_conflict=on_conflict,
                dry_run=dry_run,
            )

        return ImportResult(
            self.context,
            self,
            chunks,
            to_records=convert,
            prepare=_prepare,
            before_chunk=before_chunk,
            queue=_queue,
            total=total,
            progress=progress,
            checkpoint=checkpoint,
            on_error=on_error,
            dry_run=dry_run,
            dead_letter=dead_letter,
            signature={
                "format": format,
                "chunk_size": chunksize,
                "key": list(key_columns),
                "key_field": key_field,
            },
        )

    def from_dataframe(self, df, **opts: Any) -> "ImportResult":
        """Stream a pandas DataFrame (or chunked CSV) into this collection."""
        return self.from_records(df, format="dataframe", **opts)

    def from_csv(self, source: Any, **opts: Any) -> "ImportResult":
        """Stream a CSV source (path/URL/file or chunk iterable) into this collection."""
        return self.from_records(source, format="csv", **opts)

    def from_json(self, source: Any, **opts: Any) -> "ImportResult":
        """Stream a JSON-array file into this collection."""
        return self.from_records(source, format="json", **opts)

    def from_ndjson(self, source: Any, **opts: Any) -> "ImportResult":
        """Stream an NDJSON (JSON Lines) source into this collection."""
        return self.from_records(source, format="ndjson", **opts)

    def from_excel(self, source: Any, **opts: Any) -> "ImportResult":
        """Stream an Excel (.xlsx) worksheet into this collection."""
        return self.from_records(source, format="excel", **opts)

    # ── Verification ─────────────────────────────────────────────

    def verify_keys(self, keys: Iterable[str], *, key_field: str = "MigrationKey") -> "VerificationResult":
        """Reconcile an import: assert every key hash exists in the target.

        Uses the same keyed lookup as upsert (loads existing keys once), so it
        verifies that an idempotent import actually landed every record.
        """
        target = self.upsert_target(key_field=key_field)
        if target is None:
            raise ValueError("verify_keys requires an upsert-capable collection")
        existing = target.load_keys()
        keys = list(keys)
        return VerificationResult(checked=len(keys), missing=[key for key in keys if key not in existing])

    # ── Extension hooks ──────────────────────────────────────────

    def upsert_target(self, *, key_field: str = "MigrationKey", enforce_unique: bool = False) -> "UpsertTarget | None":
        """The keyed-import target, or ``None`` when the collection isn't keyable."""
        return None

    def _key_column(self, column: str) -> str:
        """Map a source column name to the record key used after import coercion."""
        return column

    def _resolve_source(
        self,
        source: Any,
        format: str,  # noqa: A002
        chunksize: int,
        to_records: "Callable[[Any], list[dict]] | None",
    ) -> "tuple[Iterable[Any], Callable[[Any], list[dict]], Optional[int]]":
        """Resolve ``(chunks, to_records, total)`` for a streaming import."""
        if format in ("dataframe", "csv"):
            from office365.runtime.converters.dataframe import dataframe_chunks, records_from_dataframe

            chunks, total = dataframe_chunks(source, chunksize)
            convert = to_records or (lambda chunk: records_from_dataframe(chunk))
            return chunks, convert, total
        if format == "records":
            return source, (to_records or (lambda batch: batch)), None
        records = registry.reader_for(format)(source)
        return [records], (to_records or (lambda batch: batch)), len(records)
