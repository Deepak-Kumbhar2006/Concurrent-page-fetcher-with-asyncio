"""HTTPX page fetching examples using asyncio."""
import asyncio
import httpx

async def fetch_one(client: httpx.AsyncClient, url: str) -> tuple[str, int]:
    response = await client.get(url)
    response.raise_for_status()
    return url, len(response.text)


async def fetch_all(
    client: httpx.AsyncClient, urls: list[str]
) -> list[tuple[str, int]]:
    return await asyncio.gather(*(fetch_one(client, url) for url in urls))


async def fetch_all_limited(
    client: httpx.AsyncClient, urls: list[str], limit: int = 3
) -> list[tuple[str, int]]:
    if limit <= 0:
        raise ValueError("limit must be greater than zero")
    semaphore = asyncio.Semaphore(limit)
    async def fetch_with_limit(url: str) -> tuple[str, int]:
        async with semaphore:
            return await fetch_one(client, url)

    return await asyncio.gather(*(fetch_with_limit(url) for url in urls))


async def fetch_all_safe(
    client: httpx.AsyncClient, urls: list[str], timeout: float = 0.5
) -> list[tuple[str, int | None]]:
    async def fetch_with_timeout(url: str) -> tuple[str, int | None]:
        try:
            return await asyncio.wait_for(fetch_one(client, url), timeout=timeout)
        except TimeoutError:
            return url, None
    return await asyncio.gather(*(fetch_with_timeout(url) for url in urls))
