# Import necessary libraries
import json
import traceback
from pprint import pprint

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

    def extract_body(self, raw_html: str) -> str:
        soup = BeautifulSoup(raw_html, "html.parser")

        body_content = soup.body

        if body_content:
            return str(body_content)
        return ""

    def clean_data(self, raw_html: str) -> str:
        body_content = self.extract_body(raw_html)

        # valida si no hay body
        if body_content == "":
            raise FileNotFoundError("No body content found in the provided HTML.")

        soup = BeautifulSoup(body_content, "html.parser")

        for script_or_style in soup(["script", "style"]):
            script_or_style.extract()

        cleaned_content = soup.get_text(separator="\n", strip=True)
        # print(cleaned_content)
        # cleaned_content = "\n".join(
        #     line.strip() for line in cleaned_content.splitlines() if line.strip()
        # )

        # print(">>>>>>>>>>>>>", cleaned_content)

        return cleaned_content

        # # TODO recibir url de scrape_page y validar de que web se esta escrapeando

        # for i in soup.find_all(
        #     "div", attrs={"class": "CardContainer-sc-1tt2vbg-5 fvuHxG"}
        # ):
        #     print(md(str(i), heading_style="ATX"))
        #     extracted_data.append(md(str(i), heading_style="ATX"))

        # print(md(str(divs), heading_style="ATX"))

        # print(md(divs, heading_style="ATX"))
        # print("ZZZZZZZZZZZZZ", divs[0])
        # for i in divs:
        #     print(md(str(soup), heading_style="ATX"))
        # for article in soup.find_all(
        #     "div", attrs={"class": "CardContainer-sc-1tt2vbg-5 fvuHxG"}
        # ):
        #     print(article.next_element)

        # pprint(vars(article))

        # extracted_data.append(article)

        # if title_tag and link_tag and content:
        #     extracted_data.append(
        #         {
        #             "title": title_tag.get_text(strip=True),
        #             "link": link_tag["href"],
        #             "content": content,
        #         }
        #     )

        # return extracted_data

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


# # Initialize model and messages
# model = "llama3.2"

# # Revised system message focused on structured JSON output
# system_message = {
#     "role": "system",
#     "content": "You are an AI assistant specialized in processing web content and returning structured JSON data. Always provide your response as valid, well-formatted JSON without any additional text or comments. Focus on extracting and organizing the most relevant information from websites, including main sections, key services or products, and primary navigation links.",
# }

# # User message requesting the scraping of content
# user_message = {
#     "role": "user",
#     "content": "Please scrape the content of https://www.zonaprop.com.ar/inmuebles-venta.html and provide a structured JSON response of publication values, tipe of building, currency of value, complete address, m2 and description",
# }

# # Initialize conversation with the system message and user query
# messages = [system_message, user_message]

# # First API call: Send the query and function description to the model
# response = ollama.chat(
#     model=model,
#     messages=messages,
#     tools=[
#         {
#             "type": "function",
#             "function": {
#                 "name": "query_web_scraper",
#                 "description": "Scrape the content of a web page and returns the structured JSON object with titles, articles, and associated links.",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "url": {
#                             "type": "string",
#                             "description": "The URL of the web page to scrape.",
#                         },
#                     },
#                     "required": ["url"],
#                 },
#             },
#         },
#     ],
# )

# # Append the model's response to the existing messages
# messages.append(response["message"])

# # Check if the model decided to use the provided function
# if not response["message"].get("tool_calls"):
#     print("The model didn't use the function. Its response was:")
#     print(response["message"]["content"])
# else:
#     # Process function calls made by the model
#     scraped_data = None
#     available_functions = {"query_web_scraper": query_web_scraper}

#     for tool in response["message"]["tool_calls"]:
#         function_name = tool["function"]["name"]
#         function_to_call = available_functions[function_name]
#         function_args = tool["function"]["arguments"]
#         scraped_data = function_to_call(
#             function_args["url"]
#         )  # Use await for async function call

#         print(
#             f"Function '{function_name}' was called with the URL: {function_args['url']}"
#         )

#         # Write raw HTML to file
#         write_raw_html_to_file(scraped_data["raw_html"])

#         # Add function response to the conversation
#         messages.append(
#             {
#                 "role": "tool",
#                 "name": function_name,
#                 "content": json.dumps(scraped_data),
#             }
#         )

#     if scraped_data:
#         # Additional instruction to ensure proper use of scraped data
#         additional_instruction = {
#             "role": "user",
#             "content": f"""Here's the scraped data from the website:

#             {json.dumps(scraped_data, indent=2)}

#             Using this scraped data, create a structured JSON response that includes only the most relevant and important information from the website.
#             Ignore head section. Focus on the main body section. Do not include HTML tags or unnecessary details.
#             Ensure your response is in valid JSON format without any additional text or comments.""",
#         }
#         messages.append(additional_instruction)

#         # Final API call: Get structured JSON response from the model
#         final_response = ollama.chat(model=model, messages=messages)
#         print(final_response["message"]["content"])
#     else:
#         print(
#             "No data was scraped. Unable to proceed with creating a structured JSON response."
#         )


# url = "https://www.zonaprop.com.ar/inmuebles-venta.html"

# parsed = query_web_scraper(url)

# print(html)
