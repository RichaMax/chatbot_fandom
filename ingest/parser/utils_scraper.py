import bs4

from ingest.ingest_models import Ref, Table, TableRow, Text, List
import re
from functools import reduce

HEADER_REGEX = re.compile("^h[1-6]$")

def parse_element(html_element, indentation=0):
    match html_element.name:
        case 'table':
            print(html_element['class'])
            if 'navbox' in html_element['class']:
                return []
            return [read_table(html_element)]
            return extract_table(html_element)
        case 'ul' | 'ol':
            return [List(elements=[parse_element(child) for child in html_element.find_all(recursive=False)])]
        case 'a':
            if html_element['href'] is not None:
                return [Ref(text=extract_a(html_element), link=html_element['href'])]
            else:
                return [Text(content=extract_a(html_element))]
        case x if HEADER_REGEX.match(x):
            return [Text(content=extract_header(html_element))]
        case _:
            children = html_element.contents
            if children:
                child_text_list = [
                    [Text(content=child)] if isinstance(child, str) else parse_element(child, indentation)
                    for child in children
                    if not ignore_element(child)
                ]
                return reduce(lambda x,y: x + y ,child_text_list, [])
            else:
                return [Text(content=format_raw_text(html_element))]


def ignore_element(child_element: bs4.element.Tag) -> bool:
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
        # a_img = html_cell.find("a", class_="image")
        # if a_img:
        #     return " "
    # if html_cell.get("class", "") == "headerSort":
    #     return " "
    return parse_element(html_cell)


def visible_cell(html_cell: bs4.element.Tag) -> bool:
    return "display:none" not in html_cell.get("style", "")

def read_table(html_table):
    
    rows = []
    raw_rows = html_table.find_all('tr')

    for raw_row in raw_rows:
        raw_cells = raw_row.find_all(['th', 'td'])
        cells = [extract_cell(raw_cell) for raw_cell in raw_cells]

        rows.append(TableRow(cells=cells))
    
    return Table(rows=rows)




def extract_table(html_table: bs4.element.Tag) -> str:
    # The tables used for the "Article in Progress" warning do not have a class
    # The tables at the end of articles that are not used for now have both
    # the "mw-collapsible" and "wikitable" classes
    if html_table.get("class", None) is None or all(
        class_name in html_table["class"]
        for class_name in ("mw-collapsible", "wikitable")
    ):
        return ""
    html_rows = html_table.find_all("tr")
    table_str = ""

    for row in html_rows:
        cells = row.find_all(["th", "td"])
        row_str = (
            "| "
            + " | ".join([extract_cell(cell) for cell in cells if visible_cell(cell)])
            + " |\n"
        )
        table_str += row_str
        if cells[0].name == "th":
            header_separator = "|" + "---|" * len(cells) + "\n"
            table_str += header_separator
    return table_str


def extract_header(header_html: bs4.element.Tag) -> str:
    if "pi-title" in header_html.get("class", []):
        return ""
    header_lvl = int(header_html.name[1])
    header_text = format_raw_text(header_html.find("span", class_="mw-headline"))
    return f"\n\n{'#' * header_lvl} {header_text}\n"
