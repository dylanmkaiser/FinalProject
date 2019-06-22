import pymongo

# @TODO: setup mongo connection
conn = 'mongodb://localhost:27017'

# @TODO: connect to mongo db and collection
client = pymongo.MongoClient(conn)
db = client.store_inventory
db.produce.insert_many(
[
    {
      "type": "apples",
      "cost": .23,
      "stock": 333
  },
    {
      "type": "pommes",
      "cost": .34,
      "stock": 443
  }
]
)