from flask import Flask, render_template, redirect, url_for
import pymongo
from scrape_mars import scrape
import time

app = Flask(__name__)

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define the mars_db database
db = client.mars_db

@app.route('/')
def index():
    # Obtain the Mars information from the database
    mi_dict = db.mars_info.find()

    # Render the home page
    return render_template("index.html", mi_info = mi_dict[0])


@app.route('/scrape')
def scrape_info():
    # Scrape Mars Information into a dictionary
    mars_info_dict = scrape()

    # Store the Mars information dictionary in MongoDB

    # Drop any existing data in the mars_info collection
    db.mars_info.drop()

    # Insert the Mars information into the mars_info collection
    result = db.mars_info.insert_one( mars_info_dict )
   
    # All done - Show the home page
    return redirect(url_for('.index'))

if __name__ == "__main__":
    app.run(debug=True)
