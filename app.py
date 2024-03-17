import os
from dotenv import load_dotenv
import promptlayer

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

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()