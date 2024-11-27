def split_dom_content(dom_content: str, max_lenght: int = 6000) -> list:
    return [
        dom_content[i : i + max_lenght] for i in range(0, len(dom_content), max_lenght)
    ]
