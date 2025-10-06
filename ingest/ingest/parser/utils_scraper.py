def parse_element(html_element, indentation=0):
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
            parse_element(child, indentation)
            for child in html_element.children
            if not ignore_child(child)
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
