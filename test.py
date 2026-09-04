# test.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("AQ.Ab8RN6Jq3vf0AsABehZGFYkqjhRjfkiEKixOsKhOqo6ubFl_rg")
)

# Check available models
for m in genai.list_models():
    print(m.name)
    print("Supports:", m.supported_generation_methods)
    print("----------------")