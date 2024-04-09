import asyncio

import click
import hashlib
from time import time

from ingest.generators.markdown import render
from ingest.ingestors.mongodb import MongoIngestor
from ingest.ingestors.pinecone import PineconeIngestor
from ingest.ingestors.openai import Embedder
from ingest.ingest_models import EmbeddedPage, EmbeddedChunk
from functools import wraps
from ingest_models import Page, PageMetadata
from models.mongo import Page as MongoPage, Chunk as MongoChunk
from rich.progress import track
from scraper import scrape_pages
from scraper.client import FandomClient
from scraper.page_lister import get_all_page_links, get_links_from_page
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
@click.option("--mongo", default=False, is_flag=True, help="Only save to MongoDB")
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
        urls = await get_all_page_links(fandom_client)
    elif url:
        re_result = URL_REGEX.search(url)
        domain = re_result.group(1)
        relative_url = re_result.group(2)
        urls = [relative_url]
        fandom_client = FandomClient(domain)

    scraped_pages = await scrape_pages(fandom_client, urls)

    for page in scraped_pages:
        try:
            rendered = render(page.content)
            print(rendered)
            page = Page(
            str_content=render(page.content),
            content=[element.model_dump() for element in page.content],
            metadata=PageMetadata(
                title=page.title,
                categories=page.categories,
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

    # Cut pages in chunks
    short_pages = [page for page in pages if len(page.str_content) < 20000]

    # Page -> ChunkedPage

    # Save to MongoDB

    # ChunkedPage -> EmbeddedPage

    # Save to Pinecone

    # Embed each chunk
    embedder = Embedder()

    click.echo("Embedding pages ...")

    t = time()

    embeddings = await embedder.embed([page.str_content for page in short_pages])

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
        for i, page in enumerate(short_pages)
    ]

    # Save each embedding to pinecone

    pinecone = PineconeIngestor(game)

    # pinecone.clear_index()

    pinecone.ingest_pages(embedded_pages)

    # Save the content to MongoDB
    mongo_client = MongoIngestor(game)

    # mongo.clear_collection()

    for page in track(embedded_pages, description="Saving pages to Mongo"):
        mongo_client.ingest_page(
            MongoPage(
                title=page.metadata.title,
                url=page.metadata.url,
                categories=page.metadata.categories,
                chunks=[
                    MongoChunk(
                        id=chunk.id,
                        content=chunk.content,
                    )
                    for chunk in page.chunks
                ],
            )
        )


if __name__ == "__main__":
    entrypoint()
