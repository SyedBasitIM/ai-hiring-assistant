import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from hiretalentt_profiles import ProfileManager

load_dotenv()

if __name__ == "__main__":
    if not os.getenv("MISTRAL_API_KEY"):
        print("No Mistral Api Key is found! Please check it.")
        exit(1)

    profile_manager = ProfileManager()
    profiles_data = profile_manager.get_profile_as_formatted_large_str()

    model = init_chat_model(model="mistral-large-latest", model_provider="mistralai")
    system_template = (
        "You are a recruiter assistant with access to candidate profiles. "
        "Here is the profile data:\n{profiles}\n"
        "Answer the user's question based on this data if it relates to profiles. "
        "If the question is unrelated to profiles, respond helpfully as a general assistant."
    )

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{user_query}")]
    )

    user_input = input("You: ")
    prompt = prompt_template.invoke(
        {"profiles": profiles_data, "user_query": user_input}
    )

    # response = model.invoke(prompt)
    # print(response.content)

    for chunk in model.stream(prompt):
        print(chunk.content, end="")
