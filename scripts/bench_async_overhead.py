#!/usr/bin/env python3
"""Micro-benchmark: per-request overhead of the async path vs the sync path.

Run from the repository root (no network is used)::

    uv run python scripts/bench_async_overhead.py --requests 2000 --repeat 5

Three configurations are measured on the same in-process context, each driving a
loopback transport that returns a canned JSON response:

* ``sync``   - ``ctx.execute_query()`` (baseline);
* ``async``  - ``await ctx.execute_query_async()`` with the default
  ``before_execute_async``, which offloads ``beforeExecute`` to a worker thread;
* ``inline`` - the same, but with ``before_execute_async`` replaced by an inline
  coroutine, removing the thread hop.

The ``async - inline`` delta isolates the cost of the ``beforeExecute`` worker
thread hop, which is the number that decides whether gating or optimizing that
offload is worth it.
"""

from __future__ import annotations

import argparse
import asyncio
from time import perf_counter

from office365.runtime.http.request_options import RequestOptions
from office365.runtime.transport.base import BaseTransport
from office365.sharepoint.client_context import ClientContext
from requests import Response

_SITE_URL = "https://contoso.sharepoint.com"
_BODY = b'{"d": {"Title": "bench"}}'


class _LoopbackTransport(BaseTransport):
    """Native-async no-op transport: builds a canned response with no I/O."""

    def execute(self, request: RequestOptions) -> Response:
        return self._response(request)

    async def execute_async(self, request: RequestOptions) -> Response:
        return self._response(request)

    @staticmethod
    def _response(request: RequestOptions) -> Response:
        response = Response()
        response.status_code = 200
        response.url = request.url
        response.headers["Content-Type"] = "application/json;odata=verbose"
        response._content = _BODY
        return response


def _context() -> ClientContext:
    ctx = ClientContext(_SITE_URL)
    request = ctx.pending_request()
    request.beforeExecute.clear()
    request.transport = _LoopbackTransport()
    return ctx


def _bench_sync(n: int) -> float:
    ctx = _context()
    start = perf_counter()
    for _ in range(n):
        ctx.load(ctx.web)
        ctx.execute_query()
    return perf_counter() - start


async def _bench_async(n: int, *, inline: bool) -> float:
    ctx = _context()
    if inline:

        async def _inline(_request: RequestOptions) -> None:
            pass

        ctx.pending_request().before_execute_async = _inline  # type: ignore[method-assign]

    start = perf_counter()
    for _ in range(n):
        ctx.load(ctx.web)
        await ctx.execute_query_async()
    return perf_counter() - start


def _best(fn, n: int, repeat: int) -> float:
    return min(fn(n) for _ in range(repeat))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--requests", type=int, default=2000)
    parser.add_argument("--repeat", type=int, default=5)
    args = parser.parse_args()

    sync = _best(_bench_sync, args.requests, args.repeat)
    async_ = _best(lambda n: asyncio.run(_bench_async(n, inline=False)), args.requests, args.repeat)
    inline = _best(lambda n: asyncio.run(_bench_async(n, inline=True)), args.requests, args.repeat)

    n = args.requests
    print(f"requests/run={n}  repeat={args.repeat}  (best of repeat, lower is better)")
    print(f"{'sync   execute_query':<30} {sync / n * 1e6:8.2f} us/op")
    print(f"{'async  execute_query_async':<30} {async_ / n * 1e6:8.2f} us/op")
    print(f"{'async  (inline beforeExecute)':<30} {inline / n * 1e6:8.2f} us/op")
    print(f"{'beforeExecute thread hop':<30} {(async_ - inline) / n * 1e6:8.2f} us/op")


if __name__ == "__main__":
    main()
