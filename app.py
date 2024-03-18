import os
from dotenv import load_dotenv
import promptlayer
import openai
import json
import datetime

load_dotenv('.env')
promptlayer.api_key = os.getenv("PROMPTLAYER_API_KEY")

OpenAI = promptlayer.openai.OpenAI
client = OpenAI()

today_date = datetime.datetime.now().strftime("%Y-%m-%d")
location = "New York City"

def parse_llm_response(response_message):
    if response_message.content is not None:
        print(response_message.content)
        return None
    if response_message.function_call is not None:
        if response_message.function_call.name == "calculator":
            parsed_args = json.loads(response_message.function_call.arguments)
            evaluated = eval(parsed_args['expression'])
            print("$ ", evaluated)
            return {
                "role": "function",
                "content": str(evaluated),
                "name": "calculator",
            }
        else:
            print("Function call not supported")
    return None
            

def main():
    user_input = input("Welcome to MyChatGPT! How can I help?\n> ")
    mychatgpt_prompt = promptlayer.templates.get("MyChatGPT", {
        "provider": "openai",
        "input_variables": {
            "question": user_input,
            "date": today_date,
            "location": location,
        }
    })

    response = client.chat.completions.create(
        **mychatgpt_prompt['llm_kwargs'],
        pl_tags=["mychatgpt-dev"],
    )

    response_message = response.choices[0].message
    messages = mychatgpt_prompt['llm_kwargs']['messages']
    messages.append(response_message)

    parsed_message = parse_llm_response(response_message)
    if parsed_message is not None:
        messages.append(parsed_message)

    while True:
        user_input = input("> ")
        messages.append({"role": "user", "content": user_input})

        mychatgpt_prompt['llm_kwargs']['messages'] = messages
        response = client.chat.completions.create(
            **mychatgpt_prompt['llm_kwargs'],
            pl_tags=["mychatgpt-dev"],
        )

        response_message = response.choices[0].message
        messages.append(response_message)

        parsed_message = parse_llm_response(response_message)
        if parsed_message is not None:
            messages.append(parsed_message)

if __name__ == "__main__":
    main()