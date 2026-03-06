import os
import re
import time
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from google.genai.errors import ClientError
from prompts import system_prompt
from functions.call_function import available_functions, call_function

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
retry_count = 0
for _ in range(20):
    time.sleep(12)
    try:
        response=client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
            )
        retry_count = 0    
    except ClientError as e:
        if e.code == 429:
            print("Rate limit hit.")

            # Exponential backoff with cap
            wait_time = min(2 ** retry_count, 60)

            print(f"Sleeping for {wait_time} seconds...")
            time.sleep(wait_time)

            retry_count += 1
            continue

        raise
    
    if response.candidates !=[]:
        for i in response.candidates:
            messages.append(i)

    if not response.function_calls:
        print(f"Response: {response.text}")
        break

    function_results = []   
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
            
            function_call_result= call_function(func)
            if function_call_result.parts == []:
                raise Exception("brak funkcji")
            if function_call_result.parts[0].function_response == None:
                raise Exception("brak odpowiedzi")
            if function_call_result.parts[0].function_response.response == None:
                raise Exception("brak odpowiedzi 2")
            function_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        messages.append(types.Content(role="tool", parts=function_results))
else:
    print("Error: Maximum number of iterations reached without final response.")
    exit(1)