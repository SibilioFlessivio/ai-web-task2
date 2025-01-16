from flask import Flask, request, render_template
from whoosh.qparser import QueryParser
from whoosh.index import open_dir

app = Flask(__name__)

# Open the Whoosh index
ix = open_dir("indexdir")

@app.route("/")
def home():
    return render_template("start-template.html")

@app.route("/search", methods=["POST"])
def search():
    # Get the search query from the form
    query_string = request.form.get("query")
    
    # Perform the search
    results_list = []
    with ix.searcher() as searcher:
        query = QueryParser("content_ix", ix.schema).parse(query_string)
        results = searcher.search(query)
        results.fragmenter.surround = 50
        for r in results:
            print(r.highlights("content_ix"))
            results_list.append({
                "url": r["url_ix"],
                "snippet": r.highlights("content_ix",top = 1)
            })
    
    # Render the results in a new template
    return render_template("results-template.html", query=query_string, results=results_list)
