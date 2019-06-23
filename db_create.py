import os
from dotenv import load_dotenv
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
load_dotenv()
import mysql.connector
import requests

# Database Connection
db=os.getenv("DATABASE_NAME")

try:
    mydb = mysql.connector.connect(
    host=os.getenv("DATABASE_HOST"),
    user=os.getenv("DATABASE_USERNAME"),
    passwd=os.getenv("DATABASE_PASSWORD"),
    )

    mycursor = mydb.cursor()

    mycursor.execute(f"CREATE DATABASE {db}")
    print('Database Created')
except:
    print("Database Already Exists")

mydb = mysql.connector.connect(
  host=os.getenv("DATABASE_HOST"),
  user=os.getenv("DATABASE_USERNAME"),
  passwd=os.getenv("DATABASE_PASSWORD"),
  database=os.getenv("DATABASE_NAME")
)


#=========================================
# DROP TABLES
#=========================================

print('1.  mlb_model Schema: Dropping Tables')
drop_cursor = mydb.cursor()

#order is important when dropping due to fk constraints
drop_cursor.execute('drop table if exists mlb_model.venues')
drop_cursor.execute('drop table if exists mlb_model.games')
drop_cursor.execute('drop table if exists mlb_model.pricing')



#=========================================
# CREATE TABLES
#=========================================

print('------------------------')
print('2.  mlb_model Schema: Creating tables')

mycursor = mydb.cursor()

#states table
mycursor.execute \
("create table mlb_model.venues \
  (venue_id int(10) not null\
  ,lat float \
  ,lon float \
  ,primary key (venue_id))")

mycursor.execute \
("create table mlb_model.games \
  (game_id int(10) not null\
  ,title varchar(255)\
  ,team1 varchar(255) \
  ,team2 varchar(255) \
  ,venue_id int(10)\
  ,utcdate varchar(255)\
  ,primary key (game_id))")

mycursor.execute \
("create table mlb_model.pricing \
  (game_id int(10) not null\
  ,low_price float \
  ,med_price float \
  ,high_price float \
  ,primary key (game_id))")

#Define API URL and Key
base = "https://api.seatgeek.com/2/events?"
key="MTY2Njc1Njd8MTU1ODA1NzIyNy44OQ"
start_date="2019-09-05"
sport="nfl"

#Build API String
string=f"{base}&client_id={key}&datetime_utc.gte={start_date}&type={sport}&per_page=300"
data=requests.get(string).json()

counter=0
for game in data["events"]:
    counter+=1
    #Venue Data
    venue_id=game["venue"]["id"]
    lat=game["venue"]["location"]["lat"]
    lon=game["venue"]["location"]["lon"]
    venue_data=(venue_id,lat,lon)

    #Game Data
    game_id=game["id"]
    title = game["title"]
    team1=game["performers"][0]["name"]
    team2=game["performers"][1]["name"]
    date_time=game["datetime_utc"]
    popularity=game['score']

    game_data=(game_id,title,team1,team2,date_time,venue_id)

    #Pricing Data
    low_price=game["stats"]["lowest_price"]
    med_price=game["stats"]["median_price"]
    high_price=game["stats"]["highest_price"]

    pricing_data=(game_id,low_price,med_price,high_price)

    # venueInsert = f"IF NOT EXISTS (SELECT * FROM venues WHERE venue_id ={venue_id} )\
    #                         INSERT INTO venues (venue_id, lat, lon)\
    #                         VALUES (%s, %s, %s)"
    venueInsert = "INSERT IGNORE INTO venues (venue_id, lat, lon) VALUES (%s, %s, %s)"                
    gameInsert = "INSERT INTO games (game_id, title,team1, team2, utcdate, venue_id) VALUES ( %s, %s, %s, %s, %s,%s)"
    priceInsert = "INSERT INTO pricing (game_id, low_price, med_price, high_price) VALUES (%s, %s, %s, %s)"



    mycursor.execute(venueInsert, venue_data)
    mycursor.execute(gameInsert, game_data)
    mycursor.execute(priceInsert, pricing_data)
    mydb.commit()
    print(f"Imported Game {counter}")

print('------------------------')
print('--- Job Completed ---')
