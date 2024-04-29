import os
from openai import OpenAI
from dotenv import load_dotenv
from get_token_from_vault import get_token
load_dotenv()


def convert_to_regional_language(region, content):

    messages = [
        {
            "role": "user",
            "content": (
                f"Convert this sentence into the region language of {region}. \n {content}. Print only the translated text as output."
            ),
        },
    ]
    PPLX_KEY = get_token("pvi_fb2o6zdslrsceh2hy6cteh65ak4gf5ge")
    client = OpenAI(api_key=PPLX_KEY, base_url="https://api.perplexity.ai")

    # chat completion without streaming
    response = client.chat.completions.create(
        model="mistral-7b-instruct",
        messages=messages,
    )
    print(response)
