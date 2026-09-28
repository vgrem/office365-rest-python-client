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

Bounded parallelism with progress as each file completes and per-file retry:

```python
for coro in asyncio.as_completed(tasks):
    print("[OK]", await coro)
```

### [Bulk-update list items](bulk_update_async.py)

Queue updates with synchronous builders, then let `execute_batch_async` send the
batches in parallel:

```python
await ctx.execute_batch_async(items_per_batch=100, concurrency=4, success_callback=on_batch)
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
- **Bound the fan-out.** The default transport runs blocking calls on the event
  loop's thread pool (`min(32, os.cpu_count() + 4)` workers), so an unbounded
  `gather` over thousands of requests just queues. Size an `asyncio.Semaphore`
  to what the server will tolerate.
- **Isolate failures.** Prefer `asyncio.gather(..., return_exceptions=True)` or a
  per-task `try/except` so one failed item doesn't cancel the rest.
- **Retry transient errors.** Wrap terminals in `execute_query_async_retry()`
  (or configure a shared `RateLimiter`) when driving many requests at once.
- **Batch instead of hand-rolling.** For many queued writes,
  `execute_batch_async` overlaps batches for you — no cloning needed.
