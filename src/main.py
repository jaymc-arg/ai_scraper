from ia_models.llama import parse_with_ollama
from ia_models.tokenizer import split_dom_content
from scraper import query_web_scraper


def main():
    parsed = query_web_scraper("https://www.zonaprop.com.ar/inmuebles-venta.html")

    splited_dom = split_dom_content(parsed["extracted_data"])
    print(splited_dom[0])

    parse_description = """identify the html element, by it's attribute, that contains all the relevant information of a single property. i only want the attribute name."""

    ollama_parsed = parse_with_ollama(splited_dom[2:4], parse_description)

    print(ollama_parsed)


if __name__ == "__main__":
    main()
