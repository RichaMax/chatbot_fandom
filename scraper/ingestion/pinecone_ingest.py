import asyncio
import hashlib
import time

from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from pydantic_settings import BaseSettings
from tqdm.auto import tqdm

from parser.main import parse_wiki


class Settings(BaseSettings):
    openai_api_key:str
    pinecone_api_key:str

settings = Settings()


client = OpenAI(
    api_key=settings.openai_api_key
)  # get API key from platform.openai.com

MODEL = "text-embedding-3-small"


pc = Pinecone(api_key=settings.pinecone_api_key)

spec = ServerlessSpec(cloud="aws", region="us-west-2")

index_name = 'valheim'

# check if index already exists (it shouldn't if this is your first run)
if index_name not in pc.list_indexes().names():
    # if does not exist, create index
    pc.create_index(
        index_name,
        dimension=3072,  # dimensionality of text-embed-3-small
        metric='dotproduct',
        spec=spec
    )
    # wait for index to be initialized
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)

# connect to index
index = pc.Index(index_name)
time.sleep(1)
# view index stats
index.describe_index_stats()



result = asyncio.run(parse_wiki("valheim"))
for r in result:
    meta = {"title": r.page.title,
            "categories": r.page.categories,
            "url": r.link}
    page_embeddings = client.embeddings.create(
        model="text-embedding-3-small",
        input=r.page.content).data[0].embedding
    page_data = {"id": hashlib.sha256(r.page.title.encode('utf-8')).hexdigest(),
                 "values": page_embeddings,
                 "metadata": meta}
    index.upsert([page_data])

# load the first 1K rows of the TREC dataset
# trec = load_dataset('trec', split='train[:1000]')


# count = 0  # we'll use the count to create unique IDs
# batch_size = 32  # process everything in batches of 32
# for i in tqdm(range(0, len(trec['text']), batch_size)):
#     # set end position of batch
#     i_end = min(i+batch_size, len(trec['text']))
#     # get batch of lines and IDs
#     lines_batch = trec['text'][i: i+batch_size]
#     ids_batch = [str(n) for n in range(i, i_end)]
#     # create embeddings
#     res = client.embeddings.create(input=lines_batch, model=MODEL)
#     embeds = [record.embedding for record in res.data]
#     # prep metadata and upsert batch
#     meta = [{'text': line} for line in lines_batch]
#     to_upsert = zip(ids_batch, embeds, meta)
#     # upsert to Pinecone
#     index.upsert(vectors=list(to_upsert))