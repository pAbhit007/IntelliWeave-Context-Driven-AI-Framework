from typing import List
from langchain_community.document_loaders import PyPDFium2Loader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

class PDFLoader:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

    def load_and_split(self, pdf_path: str) -> List[Document]:
        """
        Load PDF and split into chunks using PyPDFium2 (Windows compatible)
        """
        loader = PyPDFium2Loader(pdf_path)
        pages = loader.load()
        chunks = self.text_splitter.split_documents(pages)
        return chunks
