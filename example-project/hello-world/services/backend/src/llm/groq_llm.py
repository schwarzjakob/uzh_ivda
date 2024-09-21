import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class GroqClient:
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.base_url = "https://api.groq.com/openai/v1"

    def generate_poem(self, company_name, prompt_file_path):
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Load prompt file
        with open(prompt_file_path, "r") as file:
            messages_data = json.load(file)

        # Replace {company} in the prompt
        for message in messages_data["messages"]:
            message["content"] = message["content"].replace("{company}", company_name)

        # Debugging: Print the final messages sent to the API
        print(f"Final messages sent to Groq API: {messages_data['messages']}")

        # Make the API request
        response = requests.post(
            url,
            json={"model": "llama3-8b-8192", "messages": messages_data["messages"]},
            headers=headers,
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"

    def generate_additional_information(
        self, company_name, founding_year, employees, prompt_file_path
    ):
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Load prompt file
        with open(prompt_file_path, "r") as file:
            messages_data = json.load(file)

        # Replace placeholders in the prompt
        for message in messages_data["messages"]:
            message["content"] = message["content"].replace("{company}", company_name)
            message["content"] = message["content"].replace(
                "{founding_year}", str(founding_year)
            )
            message["content"] = message["content"].replace(
                "{employees}", str(employees)
            )

        # Debugging: Print the final messages sent to the API
        print(f"Final messages sent to Groq API: {messages_data['messages']}")

        # Make the API request
        response = requests.post(
            url,
            json={"model": "llama3-8b-8192", "messages": messages_data["messages"]},
            headers=headers,
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"
