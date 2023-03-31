import openai
import os
from dotenv import load_dotenv
from config_model import convert_sentence_to_config

# Set up the OpenAI API key
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

# Initialize conversation history
conversation_history = []


def add_message_to_history(user, message):
    conversation_history.append({"role": user, "content": message})


def generate_system_message(model_params):

    return f"""You are science.pal a researcher specialized in life science.
                You are an expert in wet and dry lab work in particular in 
                the field of {model_params.get('biology')}. Ask follow up questions after giving an concise answer"""


def chatbot_response(prompt):

    model_params = convert_sentence_to_config(prompt)

    # Add the prompt to the conversation history
    add_message_to_history("user", prompt)

    # Generate system message based on keywords
    system_message = generate_system_message(prompt)
    add_message_to_history("system", system_message)

    # Prepare input for the API by combining the conversation history
    input_messages = [
        {"role": message["role"], "content": message["content"]}
        for message in conversation_history
    ]

    # Call the API
    response = openai.ChatCompletion.create(
        model=model_params.get("model_type"),
        messages=input_messages,
        n=1,
        stop=None,
        temperature=model_params.get("model_temperature"),
    )

    # Extract and return the response
    reply = response.choices[0].message["content"].strip()
    add_message_to_history("assistant", reply)
    return reply
