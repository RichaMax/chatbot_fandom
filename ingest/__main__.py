import asyncio

import click
import hashlib
from time import time

from ingest.parser import parse_wiki
from ingest.ingestors.mongodb import MongoIngestor
from ingest.ingestors.pinecone import PineconeIngestor
from ingest.ingestors.openai import Embedder
from ingest.ingest_models import EmbeddedPage, EmbeddedChunk
from functools import wraps
from models.mongo import Page as MongoPage, Chunk as MongoChunk
from rich.progress import track


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
        pages = await parse_wiki(domain)
    elif url:
        raise NotImplementedError("TODO: Implement parsing a single page")

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
            metadata=page.metadata,
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
