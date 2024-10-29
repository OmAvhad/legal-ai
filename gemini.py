import requests
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


def gemini_general(my_text):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    # Prepare the payload
    payload = {"contents": {"role": "user", "parts": {"text": my_text}}}

    # Set the headers
    headers = {"Content-Type": "application/json"}

    # Make the POST request
    response = requests.post(
        url, json=payload, params={"key": api_key}, headers=headers
    )

    # Check for successful response
    if response.status_code == 200:
        # Extract the text from the response
        text = (
            response.json()
            .get("candidates")[0]
            .get("content")
            .get("parts")[0]
            .get("text")
        )
        return text
    else:
        raise Exception(
            f"Request failed with status code {response.status_code}: {response.text}"
        )


def gemini(my_text, my_function):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    # Prepare the payload
    payload = {
        "contents": {"role": "user", "parts": {"text": my_text}},
        "tools": [{"function_declarations": [my_function]}],
    }

    # Set the headers
    headers = {"Content-Type": "application/json"}

    # Make the POST request
    response = requests.post(
        url, json=payload, params={"key": api_key}, headers=headers
    )

    # Check for successful response
    if response.status_code == 200:
        # Extract the arguments from the response
        # print(response.json())
        args = (
            response.json()
            .get("candidates")[0]
            .get("content")
            .get("parts")[0]
            .get("functionCall")
            .get("args")
        )
        return args
    else:
        raise Exception(
            f"Request failed with status code {response.status_code}: {response.text}"
        )


analyze_function = {
    "name": "analyze",
    "description": (
        "You are a legal advisor. I will provide you with a text that may contain legal content. "
        "Your task is to analyze the text and identify any phrases, terms, or sections that appear "
        "suspicious, irregular, or require careful consideration. Please focus particularly on the "
        "termination clauses, with notice periods"
        "non-compete clause, assignment of intellectual property rights, and non-disclosure of information. "
        "Here is the text for analysis:"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "list": {
                "type": "array",
                "description": "The list of sentences you as a legal advisor feel are suspicious or require careful consideration.",
                "items": {
                    "type": "string",
                    "description": "Sentence that requires careful consideration.",
                },
            }
        },
        "required": ["list"],
    },
}
