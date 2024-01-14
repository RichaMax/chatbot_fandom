import asyncio
import traceback
from pathlib import Path
from time import time

import click
import httpx
from result import Err, Ok, Result
from tqdm import tqdm

from .client import FandomClient
from .page_lister import get_all_page_links
from .temp import Page
from .urls import get_sanitized_page_name_from_url
from .valheim_page_scraper import ValheimPageScraper

BATCH_SIZE = 50


@click.command()
@click.option("--url", default=None, help="The url to parse")
@click.option("--all", "domain", default=None, help="Parse all pages from the given domain")
def entrypoint(url: str | None, domain: str | None) -> None:
    if url is None and not domain:
        click.echo("Please provide a url or use the --all flag")
        return

    if domain:
        result = asyncio.run(parse_fandom_wiki(domain))
    elif url:
        raise NotImplementedError("TODO: Implement parsing a single page")
    
    # check for errors
    
    # Choose renderer

    # Pass result to renderer

async def parse_wiki(domain: str) -> list[Page]:
    client = FandomClient(domain)

    return []

async def parse_fandom_wiki(domain: str):
    output_dir = Path(f"output/{domain}")
    output_dir.mkdir(parents=True, exist_ok=True)

    pages_output_dir = output_dir / "pages"

    base_url = f"https://{domain}.fandom.com"

    client_limits = httpx.Limits(max_keepalive_connections=None, max_connections=200, keepalive_expiry=5)

    async with httpx.AsyncClient(base_url=base_url, limits=client_limits) as client:
        links = await get_all_page_links(client)
        links = links[:10]

        click.echo(f"Found {len(links)} pages")

        failed_links = []

        start = time()

        batches = [links[i : i + BATCH_SIZE] for i in range(0, len(links), BATCH_SIZE)]
        for batch in tqdm(batches):
            tasks = []
            for link in batch:
                tasks.append(try_handle_link(client, link, pages_output_dir))

            result = await asyncio.gather(*tasks)

            for link, task_result in zip(batch, result, strict=True):
                match task_result:
                    case Ok(_):
                        pass
                    case Err(e):
                        failed_links.append((link, e))

    total_time = time() - start

    if failed_links:
        error_dump = "\n-------------------------------------------------------------------------\n".join(
            [f"{link} : {error}" for link, error in failed_links]
        )

        with open(output_dir / "error_dump.txt", "w") as f:
            f.write(error_dump)

    click.echo(f"{len(links) - len(failed_links)}✔ / {len(failed_links)}✘")
    click.echo(f"Total time : {total_time}")


async def try_handle_link(client, url: str, output_folder: Path) -> Result[None, str]:
    try:
        await handle_link(client, url, output_folder)
        return Ok(None)
    except Exception:  # noqa: BLE001
        return Err(traceback.format_exc())


async def handle_link(client, url: str, output_folder: Path) -> None:
    response = await client.get(url, follow_redirects=True)
    scraper = ValheimPageScraper(response.text)
    result = scraper.scrape()

    page_filename = get_sanitized_page_name_from_url(url)

    with open(output_folder / page_filename, "w") as f:
        f.write(result)
