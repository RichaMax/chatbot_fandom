import asyncio
import traceback
from pathlib import Path

import click
from tqdm import tqdm

from ingest.parser.client import FandomClient
from ingest.parser.page_lister import get_all_page_links
from ingest.parser.scrapers.page_scraper import PageScraper
from ingest.parser.urls import get_sanitized_page_name_from_url
from ingest.parser import parse_wiki
from ingest.ingestors.mongodb import MongoIngestor
from ingest.ingestors.pinecone import PineconeIngestor
from ingest.ingestors.openai import Embedder
from ingest.ingest_models import EmbeddedPage, EmbeddedChunk
import uuid
import asyncio
from functools import wraps
from models.mongo import Page as MongoPage, Chunk as MongoChunk

# https://github.com/pallets/click/issues/85
def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper

@click.command()
@click.option("--url", default=None, help="The url to parse")
@click.option(
    "--all", "domain", default=None, help="Parse all pages from the given domain"
)
@coro
async def entrypoint(url: str | None, domain: str | None) -> None:
    if url is None and not domain:
        click.echo("Please provide a url or use the --all flag")
        return

    if domain:
        pages = await parse_wiki(domain)
    elif url:
        raise NotImplementedError("TODO: Implement parsing a single page")
    
    # Cut pages in chunks
    short_pages = [page for page in pages if len(page.str_content) < 20000]
    
    # Embed each chunk
    embedder = Embedder()

    click.echo("Embedding pages ...")

    embedded_pages = [
        EmbeddedPage(
            metadata=page.metadata,
            chunks=[
                EmbeddedChunk(
                    id=str(uuid.uuid4()),
                    content=page.str_content,
                    embedding=await embedder.embed(page.str_content),
                )
            ]
        )
        for page in tqdm(short_pages)
    ]

    # Save each embedding to pinecone

    pinecone = PineconeIngestor(domain)

    # pinecone.clear_index()

    click.echo("Saving page vectors ...")

    for page in tqdm(embedded_pages):
        pinecone.ingest_page(page)

    # Save the content to MongoDB
    mongo = MongoIngestor(domain)
    
    # mongo.clear_collection()

    click.echo("Saving pages to MongoDB ...")

    for page in tqdm(embedded_pages):
        mongo.ingest_page(
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
                ]
            )
        )

    # pages_output_dir = Path(f"output/{domain}/pages")
    # pages_output_dir.mkdir(parents=True, exist_ok=True)

    # for page in result:
    #     filename = get_sanitized_page_name_from_url(page.link) + ".md"

    #     with open(pages_output_dir / filename, "w", encoding="utf-8") as f:
    #         f.write(page.page.content)

    # check for errors

    # Choose renderer

    # Pass result to renderer


if __name__ == "__main__":
    entrypoint()