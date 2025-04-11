import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from hiretalentt_profiles import ProfileManager

load_dotenv()


class ProfileChatbot:
    def __init__(self, model, model_provider):
        self.model = init_chat_model(model=model, model_provider=model_provider)
        self.system_template = (
            "You are a recruiter assistant with access to candidate profiles. "
            "Here is the profile data:\n{profiles}\n"
            "Answer the user's question based on this data if it relates to profiles. "
            "If the question is unrelated to profiles, respond helpfully as a general assistant."
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [("system", self.system_template), ("user", "{user_query}")]
        )
        # Fetch profiles
        self.profile_manager = ProfileManager()
        self.profiles_data = self.profile_manager.get_profile_as_formatted_large_str()

    def get_prompt(self, user_query):
        return self.prompt_template.invoke({"profiles": self.profiles_data, "user_query": user_query})

    def stream_response(self, user_query):
        """Stream the response for the user's query."""
        prompt = self.get_prompt(user_query)
        for chunk in self.model.stream(prompt):
            print(chunk.content, end="")

    def respond(self, user_query):
        """Get a full response for the user's query."""
        prompt = self.get_prompt(user_query)
        response = self.model.invoke(prompt)
        return response.content

    def run_chatbot(self):
        print("How may I help you today! (type 'exit' to quit):")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("\nThanks for interacting.")
                break
            self.stream_response(user_input)
            print()


if __name__ == "__main__":
    if not os.getenv("MISTRAL_API_KEY"):
        print("No Mistral Api Key is found! Please check it.")
        exit(1)

    profile_chatbot = ProfileChatbot("mistral-large-latest", "mistralai")
    profile_chatbot.run_chatbot()

    # profile_manager = ProfileManager()
    # profiles_data = profile_manager.get_profile_as_formatted_large_str()
    #
    # model = init_chat_model(model="mistral-large-latest", model_provider="mistralai")
    # system_template = (
    #     "You are a recruiter assistant with access to candidate profiles. "
    #     "Here is the profile data:\n{profiles}\n"
    #     "Answer the user's question based on this data if it relates to profiles. "
    #     "If the question is unrelated to profiles, respond helpfully as a general assistant."
    # )
    #
    # prompt_template = ChatPromptTemplate.from_messages(
    #     [("system", system_template), ("user", "{user_query}")]
    # )
    #
    # user_input = input("You: ")
    # prompt = prompt_template.invoke(
    #     {"profiles": profiles_data, "user_query": user_input}
    # )
    #
    # # response = model.invoke(prompt)
    # # print(response.content)
    #
    # for chunk in model.stream(prompt):
    #     print(chunk.content, end="")
