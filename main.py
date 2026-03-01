import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

# Now we can access `args.user_prompt`

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("brak klucza")


client = genai.Client(api_key=api_key)
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
response=client.models.generate_content(
    model='gemini-2.5-flash', 
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    
if response.usage_metadata == None:
    raise RuntimeError("brak odpowiedzi -- brak klucza")
elif args.verbose == True:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
if response.function_calls==[] or response.function_calls==None:
    print(f"Response: {response.text}")
else:
    for func in response.function_calls:
        print(f"Calling function: {func.name}({func.args})")