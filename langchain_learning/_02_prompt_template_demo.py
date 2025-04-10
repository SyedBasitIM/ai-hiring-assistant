import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

if __name__ == '__main__':
    if not os.getenv("MISTRAL_API_KEY"):
        print("No Mistral Api Key is found! Please check it.")
        exit(1)

    model = init_chat_model(model="mistral-large-latest", model_provider="mistralai")
    user_text = input("What do you want to translate? Write the text to translate: ")
    user_selected_language = input("Provide a language to translate text into: ")
    # print(f'{language} and {text}')

    '''
    Prompt templates are a concept in LangChain designed to assist with the transformation. 
    They take in raw user input and return data (a prompt) that is ready to pass into a language model.
    '''

    # let's create a prompt template from the two user input: text, language
    system_template = "Translate the following from English into {language}"

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{text}")]
    )

    prompt = prompt_template.invoke(
        {"language": {user_selected_language}, "text": {user_text}}
    )

    response = model.invoke(prompt)
    print(response.content)

