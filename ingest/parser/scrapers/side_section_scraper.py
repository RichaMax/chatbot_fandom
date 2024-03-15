import bs4

from .scraper import Scraper


class SideSectionScraper(Scraper):
    def __init__(self, side_html: bs4.element.Tag):
        self.side_html = side_html

    def scrape(self):
        children = self.side_html.findChildren(recursive=False)
        return "".join([self.scrape_element(child) for child in children])

    def scrape_element(self, element_html):
        classes = element_html.get("class", [])
        if "pi-group" in classes:
            return self.scrape_group(element_html)
        elif "pi-panel" in classes:
            return self.scrape_panel(element_html)
        elif "pi-header" in classes:
            return self.scrape_header(element_html)
        elif "pi-data" in classes:
            return self.scrape_data(element_html)
        elif "pi-title" in classes:
            return self.scrape_title(element_html)
        else:
            # print("Scraping unknown element")
            # print(element_html)
            # print("-----------------" * 5)
            return ""

    def scrape_title(self, title_html):
        return "# " + title_html.text.strip() + "  \n"

    def scrape_data(self, data_html):
        result = ""
        children = data_html.findChildren(recursive=False)

        result += children[0].text.strip() + ": "

        value_children = children[1].findChildren(recursive=False)

        if not value_children:
            return result + children[1].text.strip() + "  \n"

        txt_children = [
            child.text.strip() for child in value_children if child.name == "a"
        ]

        result += ", ".join(txt_children)

        return result + "  \n"

    def scrape_header(self, header_html):
        return "## " + header_html.text.strip() + "  \n"

    def scrape_panel(self, panel_html):
        # print("Scraping panel")
        # print(panel_html)
        # children = panel_html.findChildren(recursive=False)
        # TODO : scrape panel
        # print([child.name for child in children])
        # print("-----------------" * 5)
        return ""

    def scrape_group(self, group_html):
        children = group_html.findChildren(recursive=False)
        return "".join([self.scrape_element(child) for child in children])
