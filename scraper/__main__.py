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
        # links = links[:10]
        # links = ["https://valheim.fandom.com/wiki/Ashlands"]

        failed_links = []

        scrape_times = []
        dl_times = []
        transform_times = []

        start = time()

        batches = [links[i : i + BATCH_SIZE] for i in range(0, len(links), BATCH_SIZE)]
        for batch in tqdm(batches):
            tasks = []
            for link in batch:
                tasks.append(try_handle_link(client, link, f"output/{domain}"))

            result = await asyncio.gather(*tasks)

            for link, task_result in zip(batch, result, strict=True):
                match task_result:
                    case Ok((dl_time, bs_time, transform_time)):
                        dl_times.append(dl_time)
                        scrape_times.append(bs_time)
                        transform_times.append(transform_time)
                    case Err(e):
                        # print(e)
                        failed_links.append((link, e))

    total_time = time() - start

    error_dump = "\n-------------------------------------------------------------------------\n".join(
        [f"{link} : {error}" for link, error in failed_links]
    )

    with open("error_dump.txt", "w") as f:
        f.write(error_dump)

    print("Nbr of failed links : ", len(failed_links))
    print("Nbr of successful links : ", len(scrape_times))
    print("Nbr of total links : ", len(links))
    print(f"Average scrape time : {sum(scrape_times) / len(scrape_times)}")
    print(f"Average download time : {sum(dl_times) / len(dl_times)}")
    print(f"Average transform time : {sum(transform_times) / len(transform_times)}")
    print(f"Total time : {total_time}")


async def try_handle_link(client, url: str, output_folder: str) -> Result[tuple[float, float, float], str]:
    try:
        return Ok(await handle_link(client, url, output_folder))
    except Exception:
        return Err(traceback.format_exc())


async def handle_link(client, url: str, output_folder: str) -> tuple[float, float, float]:
    start = time()
    response = await client.get(url, follow_redirects=True)
    html = response.text
    dl_time = time() - start
    scraper = ValheimPageScraper(html)
    bs_time = time() - start - dl_time
    result = scraper.scrape()
    transform_time = time() - start - dl_time - bs_time

    page_name = url.split("wiki/")[-1].replace("/", "-")

    filepath = Path(f"{output_folder}/{page_name}.md")

    with open(filepath, "w") as f:
        f.write(result)

    return dl_time, bs_time, transform_time
