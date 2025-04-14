import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

if __name__ == "__main__":
    # first, we need to load a file
    file_path = "../resources/Employee_Productivity_Trends_24_sample.pdf"

    if not os.path.exists(file_path):
        raise Exception("File not exist. Please verify the file path.")

    loader = PyPDFLoader(file_path)
    docs = loader.load()
    # print(len(docs))
    # print(docs[0].page_content)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=60, chunk_overlap=15, add_start_index=True  # add_start_index=True is nothing, it add one more attribute start_index to the metadata object
    )
    all_splits = text_splitter.split_documents(docs)

    # print(len(all_splits))
    print("=================")
    # for i, doc in enumerate(all_splits[:4]):
    #     print(f"Chunk {i}: {doc.page_content}... (Metadata: {doc.metadata})")
    # for i, doc in enumerate(all_splits):
    #     print(f"Chunk {i}: {doc.page_content}")

    # print(all_splits[1].page_content)
    for i in range(0, len(all_splits)):
        print(f"chunk{i}: {all_splits[i].page_content}")  # this code will also do the same as above for loop where enumerate is used.
