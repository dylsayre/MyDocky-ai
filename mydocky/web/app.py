from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    '''
    Index
    '''

    return render_template("index.html")

@app.route("/simplesearch")
def simple_search():
    return render_template("simplesearch.html")

@app.route("/documentsearch")
def document_search():
    return render_template("documentsearch.html")
