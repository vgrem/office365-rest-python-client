# Async / await

Every query that reaches the network has an async twin: build the same fluent
query, then `await ...execute_query_async()` instead of blocking the thread.
Builders stay synchronous — only the terminal call changes. No extra dependency
is required: by default the blocking HTTP call is offloaded to a worker thread,
keeping the event loop free. An optional native-async transport (httpx) is also
available.

## Query

### [Show the current user asynchronously](../sharepoint/users/whoami_async.py)

Same builder as the synchronous [whoami.py](../sharepoint/users/whoami.py) —
only the terminal call is awaited:

```python
me = await ctx.web.current_user.get().execute_query_async()
```

### [Load a web asynchronously](load_web_async.py)

```python
web = await ctx.web.get().execute_query_async()
print(web.title)
```

### [Run queries concurrently](concurrent_requests.py)

A context drains its own pending queue on each call, so overlap independent
requests across cloned contexts:

```python
web, lists = await asyncio.gather(
    web_ctx.web.get().execute_query_async(),
    lists_ctx.web.lists.get().execute_query_async(),
)
```

For many independent requests queued on **one** context, use
`ctx.execute_query_parallel_async()` — it owns the bounded fan-out and per-query
retry, so no clones or semaphores are needed. For downloads specifically, skip
the primitive and use `folder.download(dir)` (see below).

## Recipes

### [Audit every site collection concurrently](tenant_site_audit.py)

Fan out one admin call per site with a `Semaphore`, removing the N+1 sequential
loop of the synchronous counterpart. Each task clones the context, so the run
shares one token and one connection pool:

```python
async with sem:
    clone = ctx.clone(admin_site_url)
    props = await Tenant(clone).get_site_properties_by_url(site.url).execute_query_async()
```

### [Download a library concurrently](download_library_async.py)

`folder.download` enumerates the folder (paged, recursive by default), preserves
the relative tree, skips files that already exist, and downloads with bounded
concurrency — one builder, one terminal, no streams or semaphores:

```python
op = root_folder.download(output_dir, progress=report)
await op.execute_query_async(concurrency=6)
result = op.value
print(result.success, result.skipped, result.errors, len(result.failures))
```

### [Bulk-update list items](bulk_update_async.py)

Queue updates with synchronous builders, then let `execute_batch_async` send the
batches in parallel:

```python
await ctx.execute_batch_async(items_per_batch=100, concurrency=4, success_callback=on_batch)
```

### [Import a directory through a bounded pipeline](pipeline_import.py)

A producer feeds a bounded `asyncio.Queue`; worker tasks drain it, so disk reads
and uploads overlap while memory and connection usage stay flat:

```python
await queue.put((remote_name, path))  # producer blocks when the queue is full
clone = ctx.clone(site_url)  # one queue per worker
folder.upload_file(remote_name, content)
await clone.execute_query_async()
```

### [Cancel a parallel run and resume it](cancellation.py)

Cancelling `execute_query_parallel_async` re-queues the unapplied queries, so a
retry picks the work back up (at-least-once) instead of losing it:

```python
task.cancel()  # e.g. Ctrl-C or a timeout
# ... CancelledError ...
await ctx.execute_query_parallel_async()  # resumes the restored queries
```

### [Bulk-create under a shared rate limiter](rate_limited_bulk_create.py)

Opt in to fleet-wide pacing before a large write; `Retry-After` / high health
scores hold every request back as a group:

```python
ctx.with_rate_limit(health_threshold=80, min_interval=0.1)
await ctx.execute_batch_async(items_per_batch=50, concurrency=4)
```

## Integration

### [Bridge the library into FastAPI](fastapi_integration.py)

Await the terminal directly inside an ASGI handler; clone a shared context per
request so handlers never share a pending-query queue:

```python
@app.get("/users")
async def list_users(top: int = 10):
    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    users = await client.users.top(top).select(["id", "displayName"]).get().execute_query_async()
    return [{"id": u.id, "display_name": u.display_name} for u in users]
```

## Batch

### [Submit a batch asynchronously](batch_async.py)

```python
await ctx.execute_batch_async(items_per_batch=100, concurrency=4)
```

## Transports

### [Use the optional httpx transport](httpx_transport.py)

```python
ctx.pending_request().with_async_transport(HttpxTransport())
```

## Concurrency & best practices

- **One request per clone.** A context owns a single pending-query queue, so
  don't `await` two `execute_query_async()` calls on the same context at once.
  Use `ctx.clone(url)` per task: clones share credentials and the HTTP
  connection pool (one token, one session) but each has its own queue.
- **Drain many queued requests with the parallel terminal.** When the work is a
  list of independent queries (a `get()` per site), queue them and
  `await ctx.execute_query_parallel_async(concurrency=...)` — it bounds the
  fan-out and retries each query, so you don't manage clones or a `Semaphore`
  yourself. For downloads, use `folder.download(...)` (or `files.download(...)` /
  `file.download(path)`) instead — same engine, no stream management.
- **Bound the fan-out.** The default transport runs blocking calls on the event
  loop's thread pool (`min(32, os.cpu_count() + 4)` workers), so an unbounded
  `gather` over thousands of requests just queues. Size an `asyncio.Semaphore`
  (or the terminal's `concurrency`) to what the server will tolerate.
- **Isolate failures.** Prefer `asyncio.gather(..., return_exceptions=True)` or a
  per-task `try/except` so one failed item doesn't cancel the rest.
- **Retry transient errors.** Wrap terminals in `execute_query_async_retry()`
  (or configure a shared `RateLimiter`) when driving many requests at once.
- **Batch instead of hand-rolling.** For many queued writes,
  `execute_batch_async` overlaps batches for you — no cloning needed.
