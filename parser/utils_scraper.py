from abc import ABC, abstractmethod

import bs4


def parse_element(html_element: bs4.element.Tag, indentation: int = 0) -> str:
    if html_element.name == "table":
        return extract_table(html_element)
    if html_element.name and html_element.name.startswith("h"):
        if html_element.name[1].isdigit():
            return extract_header(html_element)
    if html_element.name in ["ul", "ol"]:
        return extract_list(html_element, indentation=indentation)
    if html_element.name == "a":
        return extract_a(html_element)

    if hasattr(html_element, "children"):
        child_text_list = [
            parse_element(child, indentation) for child in html_element.children if not ignore_child(child)
        ]
        full_text = "".join([child_txt for child_txt in child_text_list if child_txt])
    else:
        full_text = format_raw_text(html_element)
    return full_text


def ignore_child(child_element: bs4.element.Tag) -> bool:
    if child_element.name == "div":
        if child_element.get("id", "") == "toc":
            return True
    if child_element.name == "aside":
        return True
    if child_element.name == "figure":
        return True
    return False


def extract_a(a_html: bs4.element.Tag) -> str:
    return format_raw_text(a_html)


def format_raw_text(html_element: bs4.element.Tag) -> str:
    return html_element.get_text().replace("\n", "")


def extract_cell(html_cell: bs4.element.Tag) -> str:
    if hasattr(html_cell, "children"):
        span_ = html_cell.find("span", class_="mw-collapsible-toggle")
        if span_:
            span_.decompose()
        a_img = html_cell.find("a", class_="image")
        if a_img:
            return " "
    if html_cell.get("class", "") == "headerSort":
        return " "
    return parse_element(html_cell)


def visible_cell(html_cell: bs4.element.Tag) -> bool:
    return "display:none" not in html_cell.get("style", "")


def extract_table(html_table: bs4.element.Tag) -> str:
    # The tables used for the "Article in Progress" warning do not have a class
    # The tables at the end of articles that are not used for now have both
    # the "mw-collapsible" and "wikitable" classes
    if html_table.get("class", None) is None or all(
        class_name in html_table["class"] for class_name in ("mw-collapsible", "wikitable")
    ):
        return ""
    html_rows = html_table.find_all("tr")
    table_str = ""

    for row in html_rows:
        cells = row.find_all(["th", "td"])
        row_str = "| " + " | ".join([extract_cell(cell) for cell in cells if visible_cell(cell)]) + " |\n"
        table_str += row_str
        if cells[0].name == "th":
            header_separator = "|" + "---|" * len(cells) + "\n"
            table_str += header_separator
    return table_str


def extract_list(list_html: bs4.element.Tag, indentation: int = 0) -> str:
    html_lis = list_html.find_all("li", recursive=False)
    list_str = "\n"
    list_type = list_html.name
    indent_str = " " * indentation
    for i, li in enumerate(html_lis, start=1):
        if "mw-empty-elt" in li.get("class", []):
            continue
        if list_type == "ol":
            li_str = f"{indent_str}{i}. {parse_element(li, indentation + 1).strip()}\n"
        else:
            # ul
            li_str = f"{indent_str}* {parse_element(li, indentation + 1).strip()}\n"
        list_str += li_str

    return list_str


def extract_header(header_html: bs4.element.Tag) -> str:
    if "pi-title" in header_html.get("class", []):
        return ""
    header_lvl = int(header_html.name[1])
    header_text = format_raw_text(header_html.find("span", class_="mw-headline"))
    return f"\n\n{'#' * header_lvl} {header_text}\n"


class Scraper(ABC):
    @abstractmethod
    def scrape(self) -> str:
        ...


class SideSectionScraper(Scraper):
    def __init__(self, side_html: bs4.element.Tag):
        self.side_html = side_html

    def scrape(self) -> str:
        children = self.side_html.findChildren(recursive=False)

        result = ""

        for child in children:
            result += self.scrape_element(child)

        return result

    def scrape_element(self, element_html: bs4.element.Tag) -> str:
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

    def scrape_title(self, title_html: bs4.element.Tag) -> str:
        # print("Scraping title")
        return "# " + title_html.text.strip() + "  \n"

    def scrape_data(self, data_html: bs4.element.Tag) -> str:
        # print("Scraping data")
        # print(data_html)
        result = ""
        children = data_html.findChildren(recursive=False)
        result += children[0].text.strip() + ": "
        value_children = children[1].findChildren(recursive=False)
        if not value_children:
            return result + children[1].text.strip() + "  \n"
        txt_children = []
        for value_child in value_children:
            if value_child.name == "a":
                txt_children.append(value_child.text.strip())

        result += ", ".join(txt_children)

        return result + "  \n"

    def scrape_header(self, header_html: bs4.element.Tag) -> str:
        # print("Scraping header")
        return "## " + header_html.text.strip() + "  \n"

    def scrape_panel(self, panel_html: bs4.element.Tag) -> str:
        # print("Scraping panel")
        # print(panel_html)
        children = panel_html.findChildren(recursive=False)
        # TODO : scrape panel
        # print([child.name for child in children])
        # print("-----------------" * 5)
        return ""

    def scrape_group(self, group_html: bs4.element.Tag) -> str:
        result = ""
        # print("Scraping group")
        # print(group_html)
        children = group_html.findChildren(recursive=False)
        # print(f"Children : [child.name for child in children]")
        # print("-----------------" * 5)
        for child in children:
            # print("Scraping child")
            # print(child)
            result += self.scrape_element(child)
        return result
