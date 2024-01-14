import httpx

from .urls import get_domain_url


class FandomClient:
    def __init__(self, domain: str) -> None:
        domain_url = get_domain_url(domain)
        client_limits = httpx.Limits(
            max_keepalive_connections=None, max_connections=200, keepalive_expiry=5
        )
        self.client = httpx.AsyncClient(base_url=domain_url, limits=client_limits)
        self.redirects: dict[str, str] = {}

    async def close(self) -> None:
        await self.client.aclose()

    async def get_html(self, url: str) -> str:
        response = await self.client.get(url)

        redirects = response.history

        if redirects:
            for redirect in redirects:
                self.redirects[redirect.url.path] = response.url.path

        return response.text
