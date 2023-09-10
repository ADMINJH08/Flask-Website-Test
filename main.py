from flask import Flask, render_template, request, redirect, send_file
from extractors.wwr import extract_wwr_jobs
from file import save_to_file

app = Flask("Test Web Site")
db = {}

@app.route("/")
def home():
    return render_template("main.html")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        wwr = extract_wwr_jobs(keyword)
        jobs = wwr
        db[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in db:
        return(f"/search?keyword={keyword}")
    save_to_file(keyword,db[keyword])
    return send_file(f"{keyword}.csv", as_attachement=True)



app.run("127.0.0.1", port=8080)
