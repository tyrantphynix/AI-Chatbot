import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve your API token from the environment variable
API_TOKEN = os.environ.get("API_TOKEN")

# Using the DialoGPT-medium model for conversation
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    """
    Sends a POST request to the Hugging Face API with the provided payload.
    """
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        response_data = response.json()
    except Exception as e:
        response_data = {"error": f"Could not parse response: {e}"}
    return response_data

def chat():
    print("Welcome to the chatbot! Type 'exit' or 'quit' to end the conversation.")
    
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ['exit', 'quit']:
            print("Chatbot: Goodbye!")
            break

        # Sending the user input as payload to the model
        payload = {"inputs": user_input}
        response_data = query(payload)

        # Check for errors in the response
        if "error" in response_data:
            print("Error:", response_data["error"])
            continue

        # The response is usually a list of generated outputs
        if isinstance(response_data, list) and len(response_data) > 0:
            # DialoGPT returns a dictionary with "generated_text" key
            generated_text = response_data[0].get("generated_text", "")
            print("Chatbot:", generated_text)
        else:
            print("Chatbot:", response_data)

if __name__ == "__main__":
    chat()
