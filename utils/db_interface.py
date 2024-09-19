import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
# from ..models import OpenAIModels
# from dotenv import load_dotenv


class Database:
    '''
    Class for vector database
    '''

    def __init__(self, db: str, embeddings: OpenAIEmbeddings) -> None:
        self.db_dir = db
        self.embeddings = embeddings
        self.db = None

        def _intialize_db(self) -> Chroma:
            '''
            initialize ChromaDB with collection name for storing vectors. 
            For now collections is static, however 
            it can be added as an __init__ param later. 
            '''
            self.db = Chroma(
                collection_name="document_collection",
                embedding_function=self.embeddings,
                persist_directory=self.db,  # Where to save data locally, remove if not neccesary
            )

            return self.db

        def _load_chroma(self) -> Chroma:
            '''
            Used for loading the databse from location instead of initalizing.
            '''
            self.db = Chroma(persist_directory=self.db_dir, embedding_function=self.embeddings)
            return self.db

        if not os.listdir(self.db_dir):
            self.db = _intialize_db(self)

        else:
            self.db = _load_chroma(self)

    def delete_chroma_collection(self) -> str:
        '''
        Used for loading the databse from location instead of initalizing.
        '''
        vector_db = Chroma(persist_directory=self.db_dir, embedding_function=self.embeddings)
        vector_db.delete_collection()
        return "Successfully deleted."

    def get_files(self, file_directory: str) -> list:
        '''
        return all unique file names in the database
        '''
        return list(set([docs['source'].split(f"{file_directory}/")[1] for docs in self.db.get()['metadatas']]))

if __name__ == "__main__":
    # load_dotenv()
    # database = Database("mydocky/db", OpenAIEmbeddings(model=OpenAIModels.EMBEDDING_LARGE)).get_files("mydocky/documents")
    # print(database)
    pass
