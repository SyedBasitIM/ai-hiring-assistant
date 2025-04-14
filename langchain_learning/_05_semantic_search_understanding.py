from langchain_community.document_loaders import PyPDFLoader
import os

if __name__ == "__main__":
    file_path = "../resources/Employee_Productivity_Trends_24_sample.pdf"

    # Check if the file exists
    if not os.path.exists(file_path):
        # print(f"File not found: {file_path}")
        raise Exception(f"Pdf not found: {file_path}")
    else:
        try:
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            print(f"Number of documents loaded: {len(docs)}")
            print(docs)
        except Exception as e:
            print(f"An error occurred: {e}")

