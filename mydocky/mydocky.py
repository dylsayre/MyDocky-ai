from db_interface import Database
from embed_interface import EmbedDocs
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    db = Database("mydocky/db", OpenAIEmbeddings(model="text-embedding-3-large"))
    files = db.get_files("mydocky/documents")
    print(files)

    docs = EmbedDocs(db, "mydocky/documents")
    print(docs.documents)

    docs.embed()
