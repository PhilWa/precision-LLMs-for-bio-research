import openai
import os
from dotenv import load_dotenv

# Load your API key from an environment variable or secret management service
load_dotenv()

openai.api_key = os.getenv("API_KEY")


def use_llm(prompt: str):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return completion


#ans = use_llm("What is the role of glutamine in Hela cells")
#print(ans)
import openai
import os

# Set up the OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Initialize conversation history
conversation_history = []

def add_message_to_history(user, message):
    conversation_history.append({"role": user, "content": message})

def chatbot_response(prompt):
    # Add the prompt to the conversation history
    add_message_to_history("user", prompt)

    # Prepare input for the API by combining the conversation history
    input_messages = [{"role": message["role"], "content": message["content"]} for message in conversation_history]

    # Call the API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=input_messages,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract and return the response
    reply = response.choices[0].message['content'].strip()
    add_message_to_history("assistant", reply)
    return reply
