import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from .document_loader import DocLoader

class EmbedDocs:
    '''
    Class for embedding of documents into the ChromaDB.
    '''

    def __init__(self, db: object, directory: str) -> None:
        self.db = db
        self.directory = directory

        # Chroma.from_documents(texts, embedding=self.embedding, persist_directory=self.db.db_dir)

        def _files_to_embed(self) -> str:
            '''
            Using the provided directory return files that are not in the database.
            '''
            documents = []
            for file in os.listdir(self.directory):
                if file == ".gitkeep":
                    continue
                if file in self.db.get_files(self.directory):
                    continue
                documents.append(file)
            return documents

        self.documents = _files_to_embed(self)

        def _is_files_to_embed(self) -> bool:
            if not self.documents:
                return False
            return True

        self.is_file_to_embed = _is_files_to_embed(self)

    def embed(self):
        '''
        Embed document as a loop
        '''

        for file in self.documents:
            print(f"Attempting to Embed Document {file}...")
            doc = DocLoader.load_document(f"{self.directory}/{file}")
            Chroma.from_documents(doc, embedding=OpenAIEmbeddings(model="text-embedding-3-large"), persist_directory=self.db.db_dir)
            print(f"{file} has been embeded...")
