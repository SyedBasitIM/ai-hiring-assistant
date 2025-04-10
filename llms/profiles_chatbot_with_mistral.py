import os

from dotenv import load_dotenv
from mistralai import Mistral
from pymongo import MongoClient

load_dotenv()


class ProfileChatbot:
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model
        self.client = Mistral(api_key=api_key)
        self.conversation_history = []
        self.initialize_profile_context()

    def fetch_profiles(self):
        # print("fetching....")
        mongo_uri = os.getenv("MONGO_URI")
        # print(mongo_uri)
        client = MongoClient(mongo_uri)
        db = client["app-dev"]
        collection = db["profiles"]

        profiles = list(collection.find({}, {"_id": 0, "profileImage": 0, "seoImage": 0}))
        print(f'total profiles fetch: {len(profiles)}')

        profile_string = self.format_profiles_as_string(profiles)
        self.conversation_history.append({
            "role": "system",
            "content": profile_string
        })
        # print(f'Profiles: {len(profiles)}')

    def format_profiles_as_string(self, profiles):
        large_string = ""
        for profile in profiles:
            profile_str = "Profile: "
            profile_str += f"Name: {profile.get('firstName', 'N/A')} {profile.get('lastName', 'N/A')} |"
            profile_str += f"Area of expertise: {profile.get('areaOfExpertise', 'N/A')} |"
            profile_str += f"Current Location: {profile.get('currentLocation', 'N/A')} |"

            # Add education
            if "education" in profile and profile["education"]:
                profile_str += "Education:\n"
                for edu in profile["education"]:
                    profile_str += f"  - Degree: {edu.get('degree', 'N/A')}, Field: {edu.get('fieldOfStudy', 'N/A')}, "
                    profile_str += f"Institute: {edu.get('institute', 'N/A')}, Start: {edu.get('startDate', 'N/A')}, "
                    profile_str += f"End: {edu.get('endDate', 'N/A')}\n"

            # Add experience
            if "experience" in profile and profile["experience"]:
                profile_str += "Experience:\n"
                for exp in profile["experience"]:
                    profile_str += f"  - Position: {exp.get('position', 'N/A')}, Company: {exp.get('company', 'N/A')}, "
                    profile_str += f"Start: {exp.get('startDate', 'N/A')}, End: {exp.get('endDate', 'N/A')}\n"
                    if exp.get("practicedSkills"):
                        profile_str += "    Skills:\n"
                        for skill in exp["practicedSkills"]:
                            profile_str += f"      - Name: {skill.get('name', 'N/A')}, Category: {skill.get('category', 'N/A')}\n"
                    profile_str += f"    Responsibilities: {exp.get('responsibilityDescription', 'N/A')}\n"
                    if exp.get("projects"):
                        profile_str += "    Projects:\n"
                        for proj in exp["projects"]:
                            profile_str += f"      - {proj}\n"

            # Add current location again in full detail
            if "currentLocation" in profile and profile["currentLocation"]:
                loc = profile["currentLocation"]
                profile_str += f"Location: {loc.get('city', 'N/A')}, {loc.get('state', 'N/A')}, {loc.get('country', 'N/A')}\n"

            profile_str += "\n"  # Separator
            large_string += profile_str

        return large_string

    def run(self):
        while True:
            self.get_user_prompt()
            self.send_user_prompt_request()

    def get_user_prompt(self):
        user_prompt = input("\nYou: ")
        user_message = {
            "role": "user",
            "content": user_prompt
        }
        self.conversation_history.append(user_message)

    def send_user_prompt_request(self):

        buffer = ""
        stream_response = self.client.chat.stream(
            model=self.model,
            messages=self.conversation_history
        )
        for chunk in stream_response:
            content_part = chunk.data.choices[0].delta.content
            if content_part:
                buffer += content_part
                print(content_part, end="", flush=True)

        assistant_message = {
            "role": "assistant",
            "content": buffer
        }
        self.conversation_history.append(assistant_message)

    def initialize_profile_context(self):
        # print("fetching start")
        self.fetch_profiles()
        # print("Profile fetched!")

    @staticmethod
    def display_chatbot_instruction():
        print("\nHey! What's up? How can I help you today?")
        # print("Here’s how you can use me:")
        # print("- Type any question or prompt to start a conversation.")
        # print("- Type 'exit' or 'quit' to end the chat.\n")


if __name__ == "__main__":
    env_api_key = os.getenv("MISTRAL_API_KEY")
    if env_api_key is None:
        print("Something went wrong... Please check your Mistral API key!")
        exit(1)
    selected_model = "mistral-large-latest"
    # client = Mistral(api_key=env_api_key)
    chatbot = ProfileChatbot(env_api_key, selected_model)
    ProfileChatbot.display_chatbot_instruction()
    chatbot.run()