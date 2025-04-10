import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


def format_profiles_as_string(profiles):
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


class ProfileManager:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGO_URI")
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client["app-dev"]
        self.collection = self.db["profiles"]

    def get_profiles(self):
        profiles = list(self.collection.find({}, {"_id": 0, "profileImage": 0, "seoImage": 0}))
        return profiles
        # print(f'total profiles fetch: {len(profiles)}')

    def get_profile_as_formatted_large_str(self):
        profiles = self.get_profiles()
        return format_profiles_as_string(profiles)


# for testing...
if __name__ == '__main__':
    profile_manager = ProfileManager()
    all_profiles = profile_manager.get_profiles()
    print(all_profiles)
