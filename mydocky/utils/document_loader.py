from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, CSVLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


class DocLoader:
    '''
    return langchain document objectGetting loader information and text splitting
    '''
    
    @staticmethod
    def load_document(doc: str):
        '''
        find relevant loader to use and pass that back to Document loader
        '''
        ext = Path(doc).suffix

        extension = ext
        match extension.lower():
            case ".pdf":
                loader = PyPDFLoader(doc)
            case ".txt":
                loader = TextLoader(doc, encoding = 'UTF-8')
            case ".csv":
                loader = CSVLoader(doc, encoding = 'UTF-8')
            case _:
                raise ValueError("No loader found matching that extension")

        if loader:
            loader = loader.load()
            text_spliter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            document = text_spliter.split_documents(loader)
            return document
