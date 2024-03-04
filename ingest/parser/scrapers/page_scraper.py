import bs4

from ingest.parser.utils_scraper import parse_element
from ingest.ingest_models import ScrappedPage

from .scraper import Scraper
from .side_section_scraper import SideSectionScraper


class PageScraper(Scraper):
    def __init__(self, html: str):
        self.page_soup = bs4.BeautifulSoup(html, "html.parser")
        self.title = ""
        self.page_content = ""
        self.metadata: dict[str, list[str]] = {}

    def scrape_header(self, header_html: bs4.element.Tag | None):
        top_header = header_html.find("div", class_="page-header__categories")
        if top_header is not None:
            # self.page_content += parse_element(top_header)
            self.metadata["categories"] = [a.text for a in top_header.find_all("a")]

        header_title = header_html.find("h1", class_="page-header__title")
        self.title = header_title.text.strip()
        self.page_content += f"\n# {self.title}\n"

    def scrape_side_section(self, side_html: bs4.element.Tag | None):
        if side_html is None:
            return

        scraper = SideSectionScraper(side_html)
        self.page_content += scraper.scrape()

    def scrape_center_section(self, center_html: bs4.element.Tag) -> None:
        section_text = parse_element(center_html)
        self.page_content += section_text

    def scrape(self):
        main_html = self.page_soup.find("main", class_="page__main")
        page_header = main_html.find("div", class_="page-header")
        page_center_full = main_html.find("div", class_="mw-parser-output")
        page_side = page_center_full.find("aside", role="region")

        self.scrape_header(page_header)
        self.scrape_side_section(page_side)
        self.scrape_center_section(page_center_full)

        return ScrappedPage(content=[], str_content=self.page_content, title=self.title, categories=self.metadata["categories"])
