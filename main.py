import os
from dotenv import load_dotenv
from google import genai
import argparse

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()
# Now we can access `args.user_prompt`

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("brak klucza")

client = genai.Client(api_key=api_key)

response=client.models.generate_content(model='gemini-2.5-flash', contents=args.user_prompt)
if response.usage_metadata == None:
    raise RuntimeError("brak odpowiedzi -- brak klucza")
else:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

print(response.text)