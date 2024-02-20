import asyncio
import traceback
from pathlib import Path

import click
from tqdm import tqdm

from .client import FandomClient
from .page_lister import get_all_page_links
from .scrapers.page_scraper import PageScraper
from .temp import PageWithLink
from .urls import get_sanitized_page_name_from_url

BATCH_SIZE = 50


@click.command()
@click.option("--url", default=None, help="The url to parse")
@click.option(
    "--all", "domain", default=None, help="Parse all pages from the given domain"
)
def entrypoint(url: str | None, domain: str | None) -> None:
    if url is None and not domain:
        click.echo("Please provide a url or use the --all flag")
        return

    if domain:
        result = asyncio.run(parse_wiki(domain))
    elif url:
        raise NotImplementedError("TODO: Implement parsing a single page")

    pages_output_dir = Path(f"output/{domain}/pages")
    pages_output_dir.mkdir(parents=True, exist_ok=True)

    for page in result:
        filename = get_sanitized_page_name_from_url(page.link) + ".md"

        with open(pages_output_dir / filename, "w") as f:
            f.write(page.page)

    # check for errors

    # Choose renderer

    # Pass result to renderer


async def parse_wiki(domain: str) -> list[PageWithLink]:
    client = FandomClient(domain)

    links = await get_all_page_links(client)

    seen_urls = set()

    pages = []
    errors = []
    redirects = []

    batches = [links[i : i + BATCH_SIZE] for i in range(0, len(links), BATCH_SIZE)]
    pbar = tqdm(batches)

    for batch in pbar:
        tasks = []
        for link in batch:
            tasks.append(client.get_html(link))

        html_pages = await asyncio.gather(*tasks)

        nbr_pages = len(html_pages)

        # filter html pages for redirects
        html_pages = [page for page in html_pages if page.url not in seen_urls]

        redirects.extend(list(range(nbr_pages - len(html_pages))))

        seen_urls.update({page.url for page in html_pages})

        for page in html_pages:
            try:
                scraper = PageScraper(page.html)
                pages.append(PageWithLink(page=scraper.scrape(), link=page.url))
            except Exception:  # noqa: BLE001
                error_trace = traceback.format_exc()
                errors.append((page.url, error_trace))

        pbar.set_postfix(
            {
                "ignored redirects": len(redirects),
                "total": len(pages) + len(errors),
                "parsed": len(pages),
            }
        )

    await client.close()

    if errors:
        error_dump = "\n-------------------------------------------------------------------------\n".join(
            [f"{link} : {error}" for link, error in errors]
        )

        with open("error_dump.txt", "w") as f:
            f.write(error_dump)

    return pages
