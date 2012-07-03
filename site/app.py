from flask import Flask, render_template
import pymongo
app = Flask(__name__)

@app.route('/')
def hello():
    connection = pymongo.Connection()
    items = connection.craigslist.items
    items = {}
    
    return render_template("index.html", items=items)

if __name__ == "__main__":
    app.run()