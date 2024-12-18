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
