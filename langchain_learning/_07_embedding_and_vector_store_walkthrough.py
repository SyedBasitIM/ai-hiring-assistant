import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

if __name__ == "__main__":
    if not os.getenv("MISTRAL_API_KEY"):
        raise Exception("Mistral api key not found.")

    file_path = "../resources/Employee_Productivity_Trends_24_sample.pdf"

    if not os.path.exists(file_path):
        raise Exception("File not found.")

    # ================ loading the pdf file
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # ================ splitting the documents contents into the chunks of characters
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=120,
        chunk_overlap=20,
        add_start_index=True
    )

    split_docs = splitter.split_documents(docs)
    # print(len(split_docs))

    # ================ embedding is in progress
    embeddings = MistralAIEmbeddings(model="mistral-embed")
    # vector_1 = embeddings.embed_query(split_docs[0].page_content)
    # vector_2 = embeddings.embed_query(split_docs[1].page_content)
    # print(len(vector_1))  # will give you the dimensions like 1024, 384, 768, ...

    # ================ create vector store
    try:
        vectorstore = FAISS.from_documents(split_docs, embeddings)
    except Exception as e:
        raise Exception(f"Failed to create vector store: {e}")
    query = "What were the main metrics used to evaluate employee productivity in 2024?"
    relevant_docs = vectorstore.similarity_search(query, k=3)
    # print(len(relevant_docs))
    for i in range(0, len(relevant_docs)):
        print(f'{i}: {relevant_docs[i].page_content}')
    # this will only give you the content which is ready to send in the context of system to the llm (if I'm not wrong)

    '''
    in another file, we will add the functionality: 
        1. loading the pdf content,
        2. splitting, embedding and vector storing
        3. Then generating the response through LLM
    '''