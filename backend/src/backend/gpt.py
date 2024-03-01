from openai import AsyncOpenAI

class GPT:
    def __init__(self):
        self.openai = AsyncOpenAI()
    
    async def answer(self, question: str) -> str:
        return (await self.openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )).choices[0].message.content
    
    async def embed(self, text: str) -> list[float]:
        return await self.openai.embeddings.create(
            model="text-embedding-3-small",
            input=text
        ).data[0].embedding