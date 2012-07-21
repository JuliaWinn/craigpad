from flask import Flask, render_template
import pymongo
app = Flask(__name__)

@app.route('/')
def index():
    # establish connection
    connection = pymongo.Connection()
    
    # get cities
    cities_obj = connection.craigslist.cities
    cities = cities_obj.find()
    
    # get items
    item_obj = connection['craigslist']['items']
    items = item_obj.find(timeout=False)
    
    
    return render_template("index.html", items=items, cities=cities)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)