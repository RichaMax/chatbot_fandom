from .client import FandomClient, HtmlResult
from .page_lister import get_all_page_links
from .scrapers.page_scraper import PageScraper
import asyncio
import traceback
from ingest.ingest_models import Page, PageMetadata
from ingest.utils import cut_batches, SplitMethod
from rich.progress import track

BATCH_SIZE = 50


async def parse_wiki(domain: str) -> list[Page]:
    client = FandomClient(domain)

    links = (await get_all_page_links(client))

    seen_urls = set()

    pages = []
    errors = []
    redirects = []

    batches = cut_batches(links, batch_size=BATCH_SIZE, split=SplitMethod.FILL_LAST)
    # pbar = track(batches)

    for batch in track(batches):
        tasks = []
        for link in batch:
            tasks.append(client.get_html(link))

        html_pages = await asyncio.gather(*tasks)

        nbr_pages = len(html_pages)

        urls: dict[str, HtmlResult] = dict()
        html_pages = [
            urls.setdefault(page.url, page)
            for page in html_pages
            if page.url not in urls
        ]

        # filter html pages for redirects
        html_pages = [page for page in html_pages if page.url not in seen_urls]

        redirects.extend(list(range(nbr_pages - len(html_pages))))

        seen_urls.update({page.url for page in html_pages})

        for page in html_pages:
            try:
                scraper = PageScraper(page.html)
                scraped_page = scraper.scrape()
                pages.append(
                    Page(
                        str_content=scraped_page.str_content,
                        content=scraped_page.content,
                        metadata=PageMetadata(
                            title=scraped_page.title,
                            categories=scraped_page.categories,
                            url=page.url,
                        ),
                    )
                )
            except Exception:  # noqa: BLE001
                error_trace = traceback.format_exc()
                errors.append((page.url, error_trace))

        # pbar.set_postfix(
        #     {
        #         "ignored redirects": len(redirects),
        #         "total": len(pages) + len(errors),
        #         "parsed": len(pages),
        #     }
        # )

    await client.close()

    if errors:
        error_dump = "\n-------------------------------------------------------------------------\n".join(
            [f"{link} : {error}" for link, error in errors]
        )

        with open("output/ingest_errors.txt", "w") as f:
            f.write(error_dump)

    return pages


def parse_url(url: str) -> Page:
    ...
