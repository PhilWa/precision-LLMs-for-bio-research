import openai
import os
from dotenv import load_dotenv

# Set up the OpenAI API key
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

# Initialize conversation history
conversation_history = []

def add_message_to_history(user, message):
    conversation_history.append({"role": user, "content": message})

def generate_system_message(prompt):

    keyword_contexts = {
        "onco": "oncology",
        "microbiology": "microbiology",
        "systemsbiology": "systemsbiology",
        "cancer": "cancer",
    }

    for keyword, context in keyword_contexts.items():
        if keyword in prompt.lower():
            return f"""You are science.pal a researcher specialized in life science. 
                     You are an expert in wet and dry lab work in particular in 
                     the field of {keyword}"""

    return f"""You are science.pal a researcher specialized in life science. 
                     You are an expert in wet and dry lab practices"""


def config_model(prompt):

    if 'action::ideate' in prompt.lower():
        # TODO have a fun for prompt replace with logging.
        prompt = prompt.replace('action::ideate', "")
        return prompt, 0.75

    if 'action::plan' in prompt.lower():
        prompt = prompt.replace('action::plan', "")
        return prompt, 0.1
    
    else:
        return prompt, 0.5

def chatbot_response(prompt):

    prompt, TEMPERATURE =config_model(prompt)

    # Add the prompt to the conversation history
    add_message_to_history("user", prompt)

    # Generate system message based on keywords
    system_message = generate_system_message(prompt)
    add_message_to_history("system", system_message)

    # Prepare input for the API by combining the conversation history
    input_messages = [{"role": message["role"], "content": message["content"]} for message in conversation_history]

    # Call the API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=input_messages,
        n=1,
        stop=None,
        temperature=TEMPERATURE,
    )

    # Extract and return the response
    reply = response.choices[0].message['content'].strip()
    add_message_to_history("assistant", reply)
    return reply


