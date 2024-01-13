from bs4 import BeautifulSoup


async def get_all_page_links(client) -> list[str]:
    """Returns a list of all links to pages on the fandom wiki."""
    return await get_links_from_page(client, "/wiki/Special:AllPages")


async def get_links_from_page(client, url: str) -> list[str]:
    response = await client.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    nav = soup.find("div", class_="mw-allpages-nav")
    body = soup.find_all("div", class_="mw-allpages-body")

    assert len(body) == 1

    body = body[0]

    links = []

    for page in body.find_all("li"):
        a = page.find("a")
        relative_url = a.get("href")
        url = relative_url

        if not url.endswith(".png"):
            links.append(url)

    if nav is not None:
        if "Next page" in nav.text:
            next_page = nav.find_all("a")[-1]
            next_page_url = next_page.get("href")

            links += await get_links_from_page(client, next_page_url)

    return links
