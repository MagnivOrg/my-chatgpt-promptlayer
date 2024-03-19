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

def calculator(function_call):
  parsed_args = json.loads(function_call.arguments)
  return eval(parsed_args['expression'])

def parse_llm_response(response_message):
    if response_message.content is not None:
        print(response_message.content)
    if response_message.tool_calls is not None:
        tool_call = response_message.tool_calls[0]
        call_id = tool_call.id
        if tool_call.function.name == "calculator":
            evaluated = calculator(tool_call.function)
            print("$ ", evaluated)
            return {
                "role": "tool",
                "tool_call_id": call_id,
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