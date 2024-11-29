from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

template = (
    "You are a python beautiful Soup expert and you are tastked to obtain attribute types and names of html elemts from the following content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {{parse_description}}."
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)


model = OllamaLLM(model="llama3.2")


def parse_with_ollama(dom_chunks: str, parse_description: str) -> None:
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        # print(chunk)
        response = chain.invoke(
            {"dom_content": chunk, "parsed_description": parse_description}
        )
        print(f"Parsed_batch {i} of {len(dom_chunks)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)
