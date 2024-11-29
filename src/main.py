from ia_models.llama import parse_with_ollama
from ia_models.tokenizer import split_dom_content
from scraper import query_web_scraper


def main():
    parsed = query_web_scraper("https://www.zonaprop.com.ar/inmuebles-venta.html")

    splited_dom = split_dom_content(parsed["extracted_data"])
    print(splited_dom[0])

    parse_description = """parse the html and give me attribute name and type in a json format to replace in the following function:
    soup.find_all("div", attrs={"attribute_type": "attribute_name"})
    the selected element should contain the information of **all** the properties in the DOM. take in consideration you are not given the hole DOM.
    """

    ollama_parsed = parse_with_ollama(splited_dom[0:2], parse_description)

    print(ollama_parsed)


if __name__ == "__main__":
    main()
