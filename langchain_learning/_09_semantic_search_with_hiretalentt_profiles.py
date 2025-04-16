import os
from hiretalentt_profiles import ProfileManager
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate

load_dotenv()

if __name__ == "__main__":

    if not os.getenv("MISTRAL_API_KEY"):
        raise Exception("Mistral Api Key not found.")

    profile_manager = ProfileManager()
    profiles_data = profile_manager.get_profiles_as_formatted_large_str()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=30,
        add_start_index=True
    )

    split_text = splitter.split_text(profiles_data)
    # print(len(split_docs))

    embeddings = MistralAIEmbeddings(model="mistral-embed")

    vector_store = FAISS.from_texts(split_text, embeddings)

    print("Assistant: How may I help you today!")
    user_query = input("You: ")
    relevant_text = vector_store.similarity_search(user_query, k=3)

    model = init_chat_model(model="mistral-large-latest", model_provider="mistralai")

    system_template = (
        "You are a recruiter assistant with access to candidate profiles. "
        "Here is the profile data:\n{profiles}\n"
        "Answer the user's question based on this data if it relates to profiles. "
        "If the question is unrelated to profiles, respond helpfully as a general assistant."
    )
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", system_template),
            ("user", "{query}")
        ]
    )

    relevant_context = " ".join([text.page_content for text in relevant_text])
    prompt = prompt_template.invoke(
        {"profiles": relevant_context, "query": user_query}
    )

    print("Assistant: ")
    for chunk in model.stream(prompt):
        print(chunk.content, end="", flush=True)
