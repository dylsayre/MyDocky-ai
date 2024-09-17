from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from models import OpenAIModels # pylint: disable=import-error
from utils import Database # pylint: disable=import-error
from utils import EmbedDocs # pylint: disable=import-error
from chats import Chat

def main() -> None:
    '''
    main function
    '''

    load_dotenv()
    db = Database("mydocky/db", OpenAIEmbeddings(model=OpenAIModels.EMBEDDING_LARGE))
    files = db.get_files("mydocky/documents")
    print(files)

    docs = EmbedDocs(db, "mydocky/documents")
    print(docs.documents)

    if docs.is_file_to_embed:
        docs.embed()
    else:
        print("No files to embed")

    query = input("Please provide the question: \n")
    answer = Chat(db).similarity_search(query, k=5)

    for ans in answer:
        meta = ans[0].metadata['source'].split("/")[-1]
        print(f"Answer: \n{ans[0].page_content}\n From document: \n {meta}")

if __name__ == "__main__":
    main()
    