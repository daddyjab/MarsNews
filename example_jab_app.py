from flask import Flask, render_template
import pymongo

app = Flask(__name__)

# @TODO: setup mongo connection
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Reference the database 
db = client.store_inventory

@app.route('/')
def index():
    # @TODO: write a statement that finds all the items in the db and sets it to a variable
    food_list = list( db.produce.find() )

    # @TODO: Replace this fake data with real MongoDB data
#    food_list = [
#        {'type':'apples', 'cost':23, 'stock':333},
#        {'type':'orange', 'cost':15, 'stock':23},
#        {'type':'plums', 'cost':87, 'stock':2}
#    ]

    # Calculate the potential_revenue for each item
    # and build it into a new dictionary
    expanded_food_list = []

    for f in food_list:
        expanded_food_list.append({ **f, 'potential_revenue': f['cost'] * f['stock'] })

    # @TODO: render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", foods = expanded_food_list)

if __name__ == "__main__":
    app.run(debug=True)
