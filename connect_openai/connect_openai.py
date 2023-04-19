import openai
import os
from dotenv import load_dotenv
import pandas as pd

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
                the field of {model_params.get('biology', 'life science')}.
                Keep your answers precise and short.
                Always Always ask follow up questions and propose how you can further be of assistance."""


def chatbot_response(prompt: str, model_params: dict, abstracts: pd.DataFrame):
    # Generate system message based on keywords
    system_message = generate_system_message(model_params)
    add_message_to_history("system", system_message)

    # Here we need to inject the abstracts and weave them into the prompt
    context_instruction = " Restate the question while considering: "
    context_information = "you also consider: ".join(
        abstracts.preprint_abstract.to_list()
    )
    spiked_prompt = prompt + context_instruction + context_information

    temp_conversation_history = conversation_history.copy()
    temp_conversation_history.append({"role": "user", "content": spiked_prompt})

    temp_message = [
        {"role": message["role"], "content": message["content"]}
        for message in temp_conversation_history
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=temp_message,
        n=1,
        stop=None,
        temperature=0.2,
    )

    reply = response.choices[0].message["content"].strip()

    # Pre-pend the initial question, to maintain a sharp answer:
    reply = prompt + " " + reply

    # Now we pretend the chatgpt propmt is actually from the user
    add_message_to_history("user", reply)
    print(reply)

    # Prepare input for the API by combining the conversation history
    input_messages = [
        {"role": message["role"], "content": message["content"]}
        for message in conversation_history
    ]
    print(model_params)
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
