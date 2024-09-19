from flask import Flask, render_template, request
from dotenv import load_dotenv
from agents.agent import Agent
from utils.db_interface import Database
from utils.embed_interface import EmbedDocs
from models.dataclasses import OpenAIModels, Directories
from langchain_openai import OpenAIEmbeddings
from const import Const, EXT # pylint: disable=import-error


app = Flask(__name__)

@app.route("/")
def index():
    '''
    Index
    '''

    return render_template("index.html")

@app.route("/simplesearch", methods=["GET", "POST"])
def simple_search():
    '''
    simple search endpoint
    '''

    if request.method == "POST":
        return render_template("simplesearchrender.html", data="test")

    return render_template("simplesearch.html")

@app.route("/documentsearch", methods=["GET", "POST"])
def document_search():
    '''
    simple search endpoint
    '''
    if request.method == "POST":
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

        default_value = "Error"
        query = request.form.get('docsearch', default_value)
        print(query)
        response = Agent().start(query)
        return render_template("documentrender.html", query=query, data=response)

    return render_template("documentsearch.html")

@app.route("/upload",methods=["GET", "POST"])
def upload():
    '''
    simple search endpoint
    '''
    if request.method == "GET":
        return render_template("upload.html")
