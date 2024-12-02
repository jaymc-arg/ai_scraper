# Import necessary libraries
import json
import traceback
from pprint import pprint

import html2text
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

import ollama


# Web Scraper class definition
class WebScraper:
    def __init__(
        self, headless=False, browser_type="chromium", chunk_size=256, max_tokens=1000
    ):
        self.headless = headless
        self.browser_type = browser_type
        self.chunk_size = chunk_size
        self.max_tokens = max_tokens

    def scrape_page(self, url: str) -> str:
        with sync_playwright() as p:
            browser = getattr(p, self.browser_type).launch(
                headless=self.headless, args=["--disable-gpu", "--no-sandbox"]
            )
            context = browser.new_context()
            page = context.new_page()

            stealth_sync(page)

            # TODO VALIDAR URL y devolver tipo de url para extract_titles_articles_divs
            page.goto(url)

            html_content = page.content()
            browser.close()
        return html_content

    def extract_body(self, raw_html: str) -> BeautifulSoup:
        soup = BeautifulSoup(raw_html, "html.parser")

        body_content = soup.body

        if body_content:
            return body_content
        return ""

    def clean_data(self, raw_html: str) -> str:
        body_content = self.extract_body(raw_html)

        # valida si no hay body
        if body_content == "":
            raise FileNotFoundError("No body content found in the provided HTML.")

        # for script_or_style in soup(["script", "style"]):
        #     script_or_style.extract()

        for tag in body_content(["script", "style", "meta", "link", "noscript"]):
            tag.decompose()

        relevant_tags = [
            "div",
            "section",
            "article",
            "li",
            "span",
            "a",
        ]
        for tag in body_content.find_all(True):
            if tag.name not in relevant_tags and not any(
                child.name in relevant_tags for child in tag.descendants
            ):
                tag.decompose()

        for tag in body_content.find_all(True):  # Loop through all tags
            for attribute in [
                "style",
                # "class",
                # "id",
                "onclick",
                "data-*",
            ]:  # Add others if needed
                if attribute in tag.attrs:
                    del tag[attribute]

        for tag in body_content.find_all(True):
            if not (
                tag.get_text(strip=True)
                or any(
                    child.get_text(strip=True)
                    for child in tag.descendants
                    if child.name
                )
            ):
                tag.decompose()

        for tag in body_content.find_all(True):  # Iterate through all tags
            # Check if the tag has exactly one child and no text of its own
            while (
                len(tag.contents) == 1 and tag.contents[0].name
            ):  # comprueba que el tag tenga hijo && sea un elemento (el texto no tiene atributo.name)
                child = tag.contents[0]  # captura el hijo
                tag.replace_with(child)  # remplaza el tag de inicio con el hijo
                tag = child  # pasa la referencia del loop para coninuar el loop

        # Normalize whitespace
        cleaned_html = body_content.prettify()
        cleaned_html = " ".join(cleaned_html.split())  # Remove excessive spaces

        print(body_content.prettify())

        return str(body_content)

    # TODO recibir url de scrape_page y validar de que web se esta escrapeando

    def query_page_content(self, url: str) -> dict:
        raw_html = self.scrape_page(url)
        structured_data = {
            "url": url,
            "extracted_data": self.clean_data(raw_html),
            "raw_html": raw_html,
        }
        # print(structured_data["extracted_data"])
        return structured_data


# Function to scrape and extract data
def query_web_scraper(url: str) -> dict:
    scraper = WebScraper(headless=False)
    return scraper.query_page_content(url)


# Function to write raw HTML to file
def write_raw_html_to_file(raw_html: str, filename: str = "scraped_content.html"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(raw_html)
    print(f"Raw HTML content has been written to {filename}")
