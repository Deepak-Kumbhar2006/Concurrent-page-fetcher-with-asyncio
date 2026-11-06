"""Compare sequential and concurrent fetch timings for real web pages."""
import asyncio
import sys
import time

import httpx

from speed_run import fetch_all, fetch_all_limited, fetch_one


DEFAULT_URLS = [
    "https://docs.python.org/3/library/asyncio.html",
    "https://docs.python.org/3/library/asyncio-task.html",
    "https://docs.python.org/3/library/asyncio-sync.html",
    "https://docs.python.org/3/library/asyncio-queue.html",
    "https://docs.python.org/3/library/asyncio-stream.html",
    "https://docs.python.org/3/library/asyncio-subprocess.html",
    "https://docs.python.org/3/library/asyncio-runner.html",
    "https://docs.python.org/3/library/asyncio-eventloop.html",
    "https://docs.python.org/3/library/asyncio-protocol.html",
    "https://docs.python.org/3/library/asyncio-exceptions.html",
    "https://docs.python.org/3/library/urllib.request.html",
    "https://docs.python.org/3/library/json.html",
    "https://docs.python.org/3/library/pathlib.html",
    "https://docs.python.org/3/library/concurrent.futures.html",
    "https://docs.python.org/3/library/threading.html",
    "https://docs.python.org/3/library/http.client.html",
    "https://docs.python.org/3/library/argparse.html",
    "https://docs.python.org/3/library/time.html",
    "https://docs.python.org/3/library/collections.html",
    "https://docs.python.org/3/library/re.html",
]


async def benchmark(urls: list[str]) -> None:
    timeout = httpx.Timeout(20.0, connect=10.0)
    async with httpx.AsyncClient(
        timeout=timeout,
        follow_redirects=True,
        headers={"User-Agent": "Day03-Standalone-Asyncio-Demo/1.0"},
    ) as client:
        results = []

        async def measure(name, operation):
            start = time.perf_counter()
            pages = await operation()
            results.append((name, len(pages), time.perf_counter() - start))

        async def sequential():
            return [await fetch_one(client, url) for url in urls]

        await measure("One by one", sequential)
        await measure("All at once", lambda: fetch_all(client, urls))
        await measure("Limit 3", lambda: fetch_all_limited(client, urls, limit=3))
        await measure("Limit 10", lambda: fetch_all_limited(client, urls, limit=10))

    print(f"Fetched {len(urls)} URLs\n")
    print(f"{'Mode':<15} {'Pages':>7} {'Time (s)':>12}")
    print("-" * 36)
    for name, count, seconds in results:
        print(f"{name:<15} {count:>7} {seconds:>12.2f}")


if __name__ == "__main__":
    asyncio.run(benchmark(sys.argv[1:] or DEFAULT_URLS))
