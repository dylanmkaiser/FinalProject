# Module used to connect Python with MongoDb
import pymongo
import requests

# The default port used by MongoDB is 27017
# https://docs.mongodb.com/manual/reference/default-mongodb-port/
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define the 'classDB' database in Mongo
db = client.mlbpages

days=['01']
# ,'02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
months=['05']
# ,'06','07','08','09','10',]

for m in months:
  for d in days:

      home_abv='BAL'
      year='2018'
      month=m
      day=d




      url=f'https://www.baseball-reference.com/previews/{year}/{home_abv}{year}{month}{day}0.shtml'
      preview_id=f'{home_abv}{year}{month}{day}'
      response = requests.get(url)

# Insert a document into the 'students' collection
      db.preview.insert_one(response)
    #       {
    #         #   'preview_id': preview_id,
    #           response
    #       }
    #  )
