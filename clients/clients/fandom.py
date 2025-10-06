import httpx
from pydantic.dataclasses import dataclass
from bs4 import BeautifulSoup


@dataclass
class HtmlResult:
    url: str
    html: str

def get_domain_url(domain: str) -> str:
    return f"https://{domain}.fandom.com"


def get_sanitized_page_name_from_url(page_url: str) -> str:
    return page_url.split("wiki/")[-1].replace("/", "-")

class FandomClient:
    def __init__(self, domain: str) -> None:
        domain_url = get_domain_url(domain)
        client_limits = httpx.Limits(
            max_keepalive_connections=None, max_connections=200, keepalive_expiry=5
        )
        self.client = httpx.AsyncClient(base_url=domain_url, limits=client_limits)
        # self.redirects: dict[str, str] = {}

    async def close(self) -> None:
        await self.client.aclose()

    async def get_html(self, url: str) -> HtmlResult:
        response = await self.client.get(url, follow_redirects=True)

        # redirects = response.history
        # if redirects:
        #     for redirect in redirects:
        #         self.redirects[redirect.url.path] = response.url.path

        return HtmlResult(url=response.url.path, html=response.text)

    async def get_all_page_urls(self) -> list[str]:
        html_result = await self.get_html("/wiki/Special:AllPages")
        return await self._get_links_from_registry_html(html_result.html)

    async def _get_links_from_registry_html(self, html) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")

        nav = soup.find("div", class_="mw-allpages-nav")
        body = soup.find_all("div", class_="mw-allpages-body")[0]

        # assert len(body) == 1

        # body = body[0]

        links = []

        for page in body.find_all("li"):
            a = page.find("a")
            relative_url = a.get("href")
            url = relative_url

            if not url.endswith(".png"):
                links.append(url)

        if nav is not None and "Next page" in nav.text:
            next_page = nav.find_all("a")[-1]
            next_page_url = next_page.get("href")

            links += await self._get_links_from_registry_html((await self.get_html(next_page_url)).html)

        return links
