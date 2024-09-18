from typing import Annotated
from autogen import register_function
from models import OpenAIModels, Directories # pylint: disable=import-error
from utils import Database # pylint: disable=import-error
from langchain_openai import OpenAIEmbeddings



def register_functions(assistant, user_proxy):
    '''
    Register function for Autogen
    '''

    register_function(
        embedding_search,
        caller = assistant,
        executor = user_proxy,
        description = "Given a streamlined question search the embedded \
            vector files for the most relevant information."
    )

def embedding_search(question: Annotated[str, "Embedding vector search after \
    question is streamlined"]) -> list:
    '''
    Function call to get embeddings via question
    '''

    embeddings = []

    embedding_results = Database(
        Directories.DATABASE_DIRECTORY,
        OpenAIEmbeddings(model=OpenAIModels.EMBEDDING_LARGE)
        ).db.similarity_search_with_score(question, k=4)

    for result in embedding_results:
        embeddings.append(result[0].page_content)

    return embeddings
