from enhance_answer import enrich_metabolite_information
from connect_openai.connect_openai import chatbot_response
from references import add_ref
from utils import get_answer
import markdown


def markdownify(sentence: str) -> str:
    """Converts a given sentence into a markdown formatted string, with added support for opening links in new tabs."""
    markdown_text = markdown.markdown(sentence)
    markdown_text = markdown_text.replace("<a ", '<a target="_blank" ')
    return markdown_text


def process_input(text_input: str) -> str:
    """Processes the input text, enriches it with metabolite information if needed, generates a chatbot response, and adds reference links. Returns the response as a markdown formatted string."""
    value = enrich_metabolite_information(text_input)

    if "biogpt" in text_input.lower():
        text_input = text_input.replace("biogpt", "")
        ans = get_answer(value)[0].get("generated_text")

    else:
        value = enrich_metabolite_information(text_input)
        ans = chatbot_response(value)

    ans += "<br />"
    ans += add_ref(ans, top_n=2)

    return markdownify(ans)
