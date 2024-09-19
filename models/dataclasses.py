from enum import StrEnum

class OpenAIModels(StrEnum):
    '''
    ENUMS for OpenAI
    '''

    EMBEDDING_LARGE = "text-embedding-3-large"
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_35_TURBO = "gpt-3.5-turbo"

class Directories(StrEnum):
    '''
    ENUMS for Directories
    '''
    DOCUMENTS_DIRECTORY = "documents/"
    DATABASE_DIRECTORY = "db/"

class FlaskConst(StrEnum):
    '''
    Flask Consts
    '''

    UPLOAD_FOLDER = 'documents/'
    