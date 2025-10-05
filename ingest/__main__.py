import asyncio

import click
import hashlib
from time import time

import clients

from generators import markdown
from ingestors.db import DBIngestor
from ingestors.pinecone import PineconeIngestor
from ingestors.openai import Embedder
from ingest_models import EmbeddedPage, EmbeddedChunk
from functools import wraps
from ingest_models import Page, PageMetadata
from rich.progress import track
from parser import scrape_pages
from parser.client import FandomClient
import re


# https://github.com/pallets/click/issues/85
def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


URL_REGEX = re.compile(r"https://([a-z]*)\.fandom\.com(.*)")


@click.command()
@click.option("--url", default=None, help="The url to parse")
@click.option(
    "--all", "domain", default=None, help="Parse all pages from the given domain"
)
@click.option("--fail", default=False, is_flag=True, help="Fail on the first error")
@coro
async def entrypoint(
    url: str | None, domain: str | None, mongo: bool, fail: bool
) -> None:
    if url is None and domain is None:
        click.echo("Please provide a url or use the --all flag")
        return

    if domain:
        fandom_client = FandomClient(domain)
        urls = await fandom_client.get_all_page_urls()
    elif url:
        re_result = URL_REGEX.search(url)
        if re_result is None:
            raise Exception()
        domain = re_result.group(1)
        if domain is None:
            raise Exception()
        relative_url = re_result.group(2)
        urls = [relative_url]
        fandom_client = FandomClient(domain)
    else:
        raise Exception()

    print(f"gathered {len(urls)} urls")

    # TODO: Fetch all page htmls
    pages_html = [await fandom_client.get_html(url) for url in track(urls, description="Fetching HTML pages...")]
    pages_checksums = [hashlib.md5(html_result.html.encode()) for html_result in track(pages_html, description="Hashing pages...")]
    # TODO: Check fetched URLs and pages against what's in the database
    #        - if url exists, compare checksums.
    #            - if they don't match, remove the existing page & chunks, then pass it on to be scraped
    #        - if url doesn't exist, scrape it
    for (page_html, page_checksum) in zip(pages_html, pages_checksums):
        pass
    # TODO: Parse HTML to page representation
    scraped_pages = await scrape_pages(pages_html)
    # TODO: Implement MarkdownRenderer and use it to get text
    rendered_pages = [markdown.render(scraped_page) for scraped_page in track(scraped_pages, description="Rendering pages...")]
    # TODO: Cut each page into chunks
    chunked_pages = [chunk_page(rendered_page) for rendered_page in rendered_pages]
    # TODO: Embed each chunk and save embedding:chunk_id to qdrant
    chunks = [chunk for page in chunked_pages for chunk in page.chunks]
    embedder = Embedder()
    embeddings = embedder.embed([chunk.content for chunk in chunks])
    
    clients.vector_db.save_embeddings(embeddings)
    # TODO: Save pages and chunks to the DB
    clients.database.save_pages(chunked_pages)

    exit()

    for page in scraped_pages:
        try:
            rendered = render(page.content)
            print(rendered)
            page = Page(
                str_content=rendered,
                content=[element.model_dump() for element in page.content],
                metadata=PageMetadata(
                    title=page.title,
                    categories=page.categories,
                    checksum=hashlib.md5(rendered.encode()),
                    url=""
                ),
            )
        except Exception as e:
            print(page.title)
            print(page.content)
            print(e)
            print("---"*10)

    pages = [
        Page(
            str_content=render(page.content),
            content=[element.model_dump() for element in page.content],
            metadata=PageMetadata(
                title=page.title,
                categories=page.categories,
                url=""
            ).model_dump(),
        )
        for page in scraped_pages
    ]

    game = domain if domain is not None else url.split("/")[2]

    # TODO: Cut pages into chunks
    # Currently filtering out long pages
    chunks = [page for page in pages if len(page.str_content) < 20000]

    print(f"Scraped {len(pages)} pages")
    print(f"Got {len(chunks)} chunks")

    # Page -> ChunkedPage

    # Save to MongoDB

    # ChunkedPage -> EmbeddedPage


    # Embed each chunk
    embedder = Embedder()

    click.echo("Embedding pages ...")

    t = time()

    embeddings = await embedder.embed([page.str_content for page in chunks])

    print(f"time to embed : {time() - t}")

    embedded_pages = [
        EmbeddedPage(
            metadata=page.metadata.model_dump(),
            chunks=[
                EmbeddedChunk(
                    id=hashlib.sha256(page.metadata.title.encode("utf-8")).hexdigest()[
                        :16
                    ],
                    content=page.str_content,
                    embedding=embeddings[i],
                )
            ],
        )
        for i, page in enumerate(chunks)
    ]

    # Save each embedding to pinecone

    pinecone = PineconeIngestor(game)

    # pinecone.clear_index()

    pinecone.ingest_pages(embedded_pages)

    # Save the content to MongoDB
    db_client = DBIngestor(game)

    for page in track(embedded_pages, description="Saving pages to Mongo"):
        db_client.ingest_page(
            DBPage(
                title=page.metadata.title,
                url=page.metadata.url,
            )
        )


if __name__ == "__main__":
    entrypoint()
