import os
from flask import Flask, flash, render_template, request
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from agents.agent import Agent
from utils.db_interface import Database # pylint: disable=import-error
from utils.embed_interface import EmbedDocs # pylint: disable=import-error
from models.dataclasses import OpenAIModels, Directories, FlaskConst # pylint: disable=import-error


load_dotenv()
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = FlaskConst.UPLOAD_FOLDER

db = Database(Directories.DATABASE_DIRECTORY, OpenAIEmbeddings(model=OpenAIModels.EMBEDDING_LARGE))

UPLOAD_EXTENSIONS = {'txt', 'pdf', 'csv'}
def allowed_file(filename) -> bool:
    '''
    get allowed file from upload
    '''

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in UPLOAD_EXTENSIONS

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

        default_value = "Error"
        query = request.form.get('docsearch', default_value)
        files = db.get_files(Directories.DOCUMENTS_DIRECTORY)
        print(query)

        if not files:
            return render_template("documentrender.html", query=query,
                                    data="**No files have been uploaded, \
                                        please upload a file to do a document search**")
        response = Agent().start(query)
        return render_template("documentrender.html", query=query, data=response)

    return render_template("documentsearch.html")

@app.route("/upload",methods=["GET", "POST"])
def upload():
    '''
    simple search endpoint
    '''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return render_template("uploadrenderfail.html", file="No File Provided")
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return render_template("uploadrenderfail.html", file="No File Provided")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            docs = EmbedDocs(db, Directories.DOCUMENTS_DIRECTORY)
            if docs.is_file_to_embed:
                docs.embed()
                return render_template("uploadrendersuccess.html", file=filename)
            else:
                return render_template("uploadrenderfail.html",
                                       file="File has already been uploaded")
    return render_template("upload.html")
