import os
from dotenv import load_dotenv
import promptlayer
import openai

load_dotenv('.env')
promptlayer.api_key = os.getenv("PROMPTLAYER_API_KEY")

OpenAI = promptlayer.openai.OpenAI
client = OpenAI()

def main():
    user_input = input("Welcome to MyChatGPT! How can I help?\n> ")
    mychatgpt_prompt = promptlayer.templates.get("MyChatGPT", {
        "provider": "openai",
        "input_variables": {
            "question": user_input
        }
    })

    response = client.chat.completions.create(
        **mychatgpt_prompt['llm_kwargs'],
        pl_tags=["mychatgpt-dev"],
    )

    response_message = response.choices[0].message

    print(response_message.content)

    messages = mychatgpt_prompt['llm_kwargs']['messages']
    messages.append(response_message)
    while True:
        user_input = input("> ")
        messages.append({"role": "user", "content": user_input})

        mychatgpt_prompt['llm_kwargs']['messages'] = messages
        response = client.chat.completions.create(
            **mychatgpt_prompt['llm_kwargs'],
            pl_tags=["mychatgpt-dev"],
        )

        response_message = response.choices[0].message

        print(response_message.content)

        messages.append(response_message)

if __name__ == "__main__":
    main()