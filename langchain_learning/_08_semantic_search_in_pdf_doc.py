import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate

load_dotenv()

if __name__ == "__main__":
    file_path = "../resources/Employee_Productivity_Trends_24_sample.pdf"

    if not os.path.exists(file_path):
        raise Exception("file not found.")
    if not os.getenv("MISTRAL_API_KEY"):
        raise Exception("Mistral Api Key not found.")

    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=20,
        add_start_index=True
    )

    split_docs = splitter.split_documents(docs)
    # print(len(split_docs))

    embeddings = MistralAIEmbeddings(model="mistral-embed")

    vector_store = FAISS.from_documents(split_docs, embeddings)

    query = "What is the average focus time per day across employees?"
    relevant_docs = vector_store.similarity_search(query, k=2)
    # print(f'0: {relevant_docs[0].page_content}')
    # print(f'1: {relevant_docs[1].page_content}')

    model = init_chat_model(model="mistral-large-latest", model_provider="mistralai")

    system_template = (
        "You are an assistant answering questions based on this PDF content:\n{context}\n"
        "Provide the answer. If the question is unrelated, respond helpfully."
    )
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", system_template),
            ("user", "{text}")
        ]
    )

    relevant_context = " ".join([doc.page_content for doc in relevant_docs])
    prompt = prompt_template.invoke(
        {"context": relevant_context, "text": query}
    )

    print("Assistant: ")
    for chunk in model.stream(prompt):
        print(chunk.content, end="", flush=True)
