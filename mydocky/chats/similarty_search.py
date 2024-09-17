class Chat:
    '''
    Chat class.
    '''
    def __init__(self, db: object) -> None:
        '''
        initialize the database here and embed any documents 
        that do not exist in the database, but are in the documents folder.
        '''

        self.db = db

    def similarity_search(self, query: str, k: int):
        '''
        Simple ChromaDB similarity search
        '''

        return self.db.similarity_search_with_score(query, k)



if __name__ == "__main__":
    pass
