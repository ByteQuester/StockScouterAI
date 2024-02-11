import os

import openai


def set_openai_key(api_key):
    openai.api_key = api_key
    os.environ["OPENAI_API_KEY"] = api_key
