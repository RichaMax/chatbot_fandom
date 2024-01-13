import asyncio
import traceback
from pathlib import Path
from time import time

import httpx
from result import Err, Ok, Result
from tqdm import tqdm

from .temp import get_all_page_links
from .valheim_page_scraper import ValheimPageScraper

BATCH_SIZE = 50


def main():
    asyncio.run(parse_fandom_wiki("valheim"))


async def parse_fandom_wiki(domain: str):
    output_dir = Path(f"output/{domain}")
    output_dir.mkdir(parents=True, exist_ok=True)

    base_url = f"https://{domain}.fandom.com"

    client_limits = httpx.Limits(max_keepalive_connections=None, max_connections=200, keepalive_expiry=5)

    async with httpx.AsyncClient(base_url=base_url, limits=client_limits) as client:
        links = await get_all_page_links(client)

        failed_links = []


        start = time()

        batches = [links[i : i + BATCH_SIZE] for i in range(0, len(links), BATCH_SIZE)]
        for batch in tqdm(batches):
            tasks = []
            for link in batch:
                tasks.append(try_handle_link(client, link, f"output/{domain}"))

            result = await asyncio.gather(*tasks)

            for link, task_result in zip(batch, result, strict=True):
                match task_result:
                    case Ok(_):
                        pass
                    case Err(e):
                        failed_links.append((link, e))

    total_time = time() - start

    error_dump = "\n-------------------------------------------------------------------------\n".join(
        [f"{link} : {error}" for link, error in failed_links]
    )

    with open("error_dump.txt", "w") as f:
        f.write(error_dump)

    print(f"{len(links) - len(failed_links)}✔ / {len(failed_links)}✘")
    print(f"Total time : {total_time}")


async def try_handle_link(client, url: str, output_folder: str) -> Result[None, str]:
    try:
        return Ok(await handle_link(client, url, output_folder))
    except Exception:  # noqa: BLE001
        return Err(traceback.format_exc())


async def handle_link(client, url: str, output_folder: str) -> None:
    response = await client.get(url, follow_redirects=True)
    scraper = ValheimPageScraper(response.text)
    result = scraper.scrape()

    page_name = url.split("wiki/")[-1].replace("/", "-")

    filepath = Path(f"{output_folder}/{page_name}.md")

    with open(filepath, "w") as f:
        f.write(result)

    return None
