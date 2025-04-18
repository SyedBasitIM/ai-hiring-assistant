import getpass
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

if __name__ == '__main__':
    # if not os.environ.get("MISTRAL_API_KEY"):
    #     os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")
    if not os.getenv("MISTRAL_API_KEY"):
        print("No Mistral Api Key is found! Please check it.")
        exit(1)

    # This code sets up a Mistral AI model to translate text from English to Hindi using LangChain.
    # It sends a system instruction and a user message, then prints the response in two ways: all at once and word-by-word (streaming).
    model = init_chat_model("mistral-large-latest", model_provider="mistralai")
    messages = [
        SystemMessage("Translate the following from English into hindi"),
        HumanMessage("I am Syed Basit. I will start playing cricket after clocking 8 hours of work."),
    ]

    response = model.invoke(messages)
    print(response)  # Prints the full response object (includes metadata)
    # print(response.pretty_print())  # This to format the response nicely
    print(response.content)  # Prints just the translated text, in the sense what ever the translation will be generated by mistral here whether it's translation along with explaintion.

    # Now with streaming: This loops through the response and prints it word-by-word as it arrives
    for chunk in model.stream(messages):
        # print(chunk, end="")  # Prints the full chunk object (similar to 'response' above)
        print(chunk.content, end="")  # Prints just the translated text, word-by-word, without a newline
