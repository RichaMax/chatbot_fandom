import asyncio
from contextlib import contextmanager

import click
import hashlib
from time import time
from typing import Iterator

import clients

from generators import markdown
from ingestors.openai import Embedder
from functools import wraps
from ingest_models import Page, PageMetadata, ChunkedPage
from rich.progress import track, Progress, SpinnerColumn, TimeElapsedColumn, TextColumn
from parser import parse_page
from parser.client import FandomClient
import re


# https://github.com/pallets/click/issues/85
def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


URL_REGEX = re.compile(r"https://([a-z]*)\.fandom\.com(.*)")

def chunk_page(page: str) -> ChunkedPage:
    return []

@contextmanager
def spinner(description: str) -> Iterator[Progress]:
    progress = Progress(
        SpinnerColumn(),
        TextColumn("{task.description}"),
        TimeElapsedColumn(),
    )
    progress.add_task(description)
    yield progress
    
    
@click.command()
@click.option("--url", default=None, help="The url to parse")
@click.option(
    "--all", "domain", default=None, help="Parse all pages from the given domain"
)
@click.option("--fail", default=False, is_flag=True, help="Fail on the first error")
@coro
async def entrypoint(
    url: str | None, domain: str | None, fail: bool
) -> None:
    if url is None and domain is None:
        click.echo("Please provide a url or use the --all flag")
        return

    if domain:
        fandom_client = FandomClient(domain)
        urls = await fandom_client.get_all_page_urls()
        print(f"gathered {len(urls)} urls")
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

    game = domain if domain is not None else url.split("/")[2]

    vector_db = clients.vector_db.VectorDatabase()
    await vector_db.get_or_create_collection(game)
    db = clients.database.Database()


    pages_html = [
        await fandom_client.get_html(url)
        for url in track(urls, description="Fetching HTML pages...")
    ]
    pages_checksums = [
        hashlib.md5(html_result.html.encode())
        for html_result in track(pages_html, description="Hashing pages...")
    ]
    db_checksums = await db.get_checksums_by_urls(urls)
    pages_to_parse = [
        page_html
        for (page_html, page_checksum, db_checksum) in zip(pages_html, pages_checksums, db_checksums)
        if page_checksum != db_checksum
    ]
    # TODO: Remove existing pages

    parsed_pages = [parse_page(page) for page in track(pages_to_parse, description="Parsing pages...")]
    # Trop rapide pour etre track jpense
    rendered_pages = [
        markdown.render(parsed_page)
        for parsed_page in track(parsed_pages, description="Rendering pages...")
    ]
    # Trop rapide pour etre track jpense
    chunked_pages = [
        chunk_page(rendered_page)
        for rendered_page in track(rendered_pages, description="Chunking pages...")
    ]
    chunks = [chunk for page in chunked_pages for chunk in page.chunks]

    with spinner("Embedding..."):
        embedder = Embedder()
        embeddings = await embedder.embed([chunk.content for chunk in chunks])
    
    with spinner("Storing embeddings..."):
        await vector_db.save_embeddings(game, [chunk.id for chunk in chunks], embeddings)
        
    with spinner("Storing pages..."):
        await db.store_chunked_pages(chunked_pages)


if __name__ == "__main__":
    entrypoint()
