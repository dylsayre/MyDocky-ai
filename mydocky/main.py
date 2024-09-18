import sys
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from models import OpenAIModels, Directories # pylint: disable=import-error
from utils import Database # pylint: disable=import-error
from utils import EmbedDocs # pylint: disable=import-error
from chats import Chat
from agents import Agent # pylint: disable=import-error

def main() -> None:
    '''
    main function
    '''

    load_dotenv()
    db = Database(Directories.DATABASE_DIRECTORY, OpenAIEmbeddings(model=OpenAIModels.EMBEDDING_LARGE))
    files = db.get_files(Directories.DOCUMENTS_DIRECTORY)
    print(files)

    docs = EmbedDocs(db, Directories.DOCUMENTS_DIRECTORY)
    print(docs.documents)

    if docs.is_file_to_embed:
        docs.embed()
    else:
        print("No files to embed")

    while True:
        query = input("Please provide the question: \n")
        if query == "quit":
            sys.exit(0)
        answer = Agent().start(query)
        print(f"The Final Answer: {answer}")

    #for ans in answer:
    #    meta = ans[0].metadata['source'].split("/")[-1]
    #    print(f"Answer: \n{ans[0].page_content}\n From document: \n {meta}")

if __name__ == "__main__":
    main()
