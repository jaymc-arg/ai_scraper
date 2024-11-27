from ia_models.llama import parse_with_ollama
from ia_models.tokenizer import split_dom_content
from scraper import query_web_scraper


def main():
    parsed = query_web_scraper("https://www.zonaprop.com.ar/inmuebles-venta.html")

    splited_dom = split_dom_content(parsed["extracted_data"])

    parse_description = "for each publication extract the price of the house, currency, m2, complete address"

    ollama_parsed = parse_with_ollama(splited_dom, parse_description)

    print(ollama_parsed)


if __name__ == "__main__":
    main()
