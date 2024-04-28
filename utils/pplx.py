import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def convert_to_regional_language(content):

    messages = [
    
        {
            "role": "user",
            "content": (
                "How many stars are in the universe?"
            ),
        },
    ]

    client = OpenAI(api_key=os.getenv('PPLX_KEY'), base_url="https://api.perplexity.ai")

    # chat completion without streaming
    response = client.chat.completions.create(
        model="mistral-7b-instruct",
        messages=messages,
    )
    print(response)

