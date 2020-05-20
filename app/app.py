from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
 
 # Or set inline
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#need this to make an html
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)

#get the data to put into the html
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    #call function to scrape all the data
    marsData = scrapeAll()
    #insert it
    mars.replace_one(marsData,upsert = True)
    return "success"

if __name__ == "__main__":
    app.run(debug=True)