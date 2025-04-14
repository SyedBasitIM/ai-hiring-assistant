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
            print(f"Number of documents loaded: {len(docs)}") # len(docs) will count the number of documents or pages in the loaded pdf/file.
            print(docs) # This will print the list of Document object basically Document(page_content, metadata={dictionary})
            print(docs[0]) # This will print the page_content and metadata of first page
        except Exception as e:
            print(f"An error occurred: {e}")

    # print(f"{docs[0].page_content[:200]}\n") # This will print the first 200 characters of the first page
    # print(f"{docs[0].page_content[0:]}\n") # This will print the characters till the end from the 0th index
    # print(f"{docs[0].page_content}\n") # This will print all the content of first page
    # print(docs[2].page_content) # This will print all the content of 3 page if exits else index out of range error occur