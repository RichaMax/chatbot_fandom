from ingest.ingest_models import Ref, Text, List, Table, PageContent

def render(page_content: PageContent) -> str:
    print(f"RENDERING {page_content}")
    result = ""

    for element in page_content:
        match element:
            case Text():
                result += render_text(element)
            case Ref():
                result += render_ref(element)
            case List():
                result += render_list(element)
            case Table():
                result += render_table(element)
            case _:
                print("FALLBACK")
    
    return result

def render_text(text: Text) -> str:
    return text.content

def render_ref(ref: Ref) -> str:
    return f"[{ref.text}]({ref.link})"

def render_list(elements: List) -> str:
    result = ''
    for element in elements.elements:
        result += f' * {render(element)}\n'
    return result

def render_table(table: Table) -> str:
    result = ""
    header_row = table.rows[0]
    headers = [render(header) for header in header_row.cells]
    result += "| " + " | ".join(headers) + " |\n"
    result += "| " + " | ".join("-"*len(header) for header in headers) + " |\n"
    for row in table.rows[1:]:
        rendered_row = [render(element) for element in row.cells]
        result += "|" + " | ".join(rendered_row) + " |\n"
    
    return result
