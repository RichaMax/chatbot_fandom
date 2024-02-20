def get_domain_url(domain: str) -> str:
    return f"https://{domain}.fandom.com"


def get_sanitized_page_name_from_url(page_url: str) -> str:
    return page_url.split("wiki/")[-1].replace("/", "-")
