from .client import FandomClient
from .page_lister import get_all_page_links
from .scrapers.page_scraper import PageScraper
from tqdm import tqdm
import asyncio
import traceback
from ingest.ingest_models import Page, PageMetadata

BATCH_SIZE = 50

async def parse_wiki(domain: str) -> list[Page]:
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
                scraped_page = scraper.scrape()
                pages.append(Page(str_content=scraped_page.str_content, content=scraped_page.content, metadata=PageMetadata(title=scraped_page.title, categories=scraped_page.categories, url=page.url)))
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

def parse_url(url: str) -> Page:
    ...