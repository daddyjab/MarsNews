import pymongo

# @TODO: setup mongo connection
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Reference the database 
db = client.store_inventory

food_list = [
    {'type':'apples', 'cost':23, 'stock':333},
    {'type':'orange', 'cost':15, 'stock':23},
    {'type':'plums', 'cost':87, 'stock':2},
    {'type':'starfruit', 'cost':2, 'stock':76},
    {'type':'guava', 'cost':34, 'stock':2232}
]

db.produce.insert_many(food_list)

