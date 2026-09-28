# Async / await

Run the same fluent API from `async` code. Builders stay synchronous — only the
terminal calls that hit the network gain an `_async` twin that you `await`:

| Synchronous | Asynchronous |
|---|---|
| `ctx.execute_query()` | `await ctx.execute_query_async()` |
| `obj.execute_query()` | `await obj.execute_query_async()` |
| `ctx.execute_query_retry()` | `await ctx.execute_query_async_retry()` |
| `ctx.execute_batch()` | `await ctx.execute_batch_async()` |

No extra dependency is required. By default the blocking HTTP call is handed to
a worker thread, so the event loop stays free and existing transports (session,
auth, proxies, rate limiting) are reused unchanged.

## Quick start

```python
import asyncio

from office365.sharepoint.client_context import ClientContext

ctx = ClientContext(site_url).with_username_and_password(tenant, client_id, username, password)


async def main() -> None:
    web = await ctx.web.get().execute_query_async()
    print(web.title)


asyncio.run(main())
```

`execute_query_async()` returns the same object as its synchronous twin, so the
patterns you already use (`await ctx.web.get().execute_query_async()`, reading
`.value`, chaining) are unchanged.

## Concurrency

A context drains its own pending query queue on every call. To run independent
requests concurrently, give each one its own [cloned](getting-started.md) context
(the clone shares credentials and the connection pool) and await them together:

```python
web_ctx = ctx.clone(site_url)
lists_ctx = ctx.clone(site_url)

web, lists = await asyncio.gather(
    web_ctx.web.get().execute_query_async(),
    lists_ctx.web.lists.get().execute_query_async(),
)
```

For many queued operations, prefer the batch API below — it overlaps batches
without hand-managing contexts.

## Recipes

End-to-end examples that show where async pays off:

- [Audit every site collection concurrently](products/async/tenant_site_audit.md) —
  bounded fan-out over a tenant, replacing an N+1 sequential loop.
- [Download a library concurrently](products/async/download_library_async.md) —
  progress as each file finishes, per-file retry.
- [Bulk-update list items](products/async/bulk_update_async.md) —
  `execute_batch_async` sends the batches in parallel.
- [Show the current user](products/sharepoint/users/whoami_async.md) — the
  minimal async query, the `await` twin of `whoami.py`.

## Batch

`execute_batch_async()` splits pending changes exactly like `execute_batch()` and
runs each batch off the event loop. With `concurrency` > 1 the batches overlap,
and throttling / per-sub-request retry (including honoring `Retry-After`) behave
as in the synchronous path:

```python
target_list = ctx.web.lists.get_by_title("Company Tasks")
for index in range(250):
    target_list.add_item({"Title": f"Task {index}"})

await ctx.execute_batch_async(items_per_batch=100, concurrency=4)
```

Graph's JSON batch keeps its `sequential=True` option (chained `dependsOn`)
exactly as the synchronous method:

```python
await client.execute_batch_async(items_per_batch=20, sequential=True)
```

## Retry

`execute_query_async_retry()` mirrors `execute_query_retry()` but waits between
attempts with `asyncio.sleep`, so other tasks keep running:

```python
await ctx.execute_query_async_retry(max_retry=5, timeout_secs=5, max_delay=60)
```

The retry policy mirrors `execute_query_retry` exactly: transient errors
(408/429/5xx and connection errors) are retried with exponential backoff and
jitter. Pass a `failure_callback` (for example returning the server's
`Retry-After` via `retry_after_delay`) to override the backoff.

## Async context manager

`ClientContext` can be used as an async context manager; on exit the transport is
closed without blocking the loop:

```python
async with ctx:
    web = await ctx.web.get().execute_query_async()
```

## Optional native-async transport

The default transport offloads blocking `requests` calls to a thread. If you
prefer genuinely asynchronous I/O, install the optional
[`httpx`](https://www.python-httpx.org/) extra and select it for the async path
only — synchronous calls keep using `requests`:

```bash
pip install office365-rest-python-client[httpx]
```

```python
from office365.runtime.transport.httpx_transport import HttpxTransport

ctx.pending_request().with_async_transport(HttpxTransport())
try:
    web = await ctx.web.get().execute_query_async()
finally:
    await ctx.pending_request().async_transport.aclose()
```

!!! note "Limits of the httpx transport"
    Responses are adapted to `requests.Response`, so downstream code is
    unchanged, but the body is read eagerly (streamed downloads work via
    `iter_content` yet are buffered in memory). TLS verification, proxies and
    redirect policy are client-level constructor settings; per-request `verify`
    and `proxies` are not honored.

## Notes

- Async support is additive: nothing in the synchronous API changed, and both
  paths can share one context. Builders remain synchronous; call them before
  `await`ing.
- The async batch path runs the existing (synchronous) batch machinery off the
  loop, so it currently uses the request's synchronous transport even when an
  async transport is configured.
- `retry_async()` and the async terminals are available from
  `office365.runtime.retry` and the usual query objects.

See the runnable [async examples](products/async/index.md).
