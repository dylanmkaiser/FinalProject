import os
from dotenv import load_dotenv
load_dotenv()
import mysql.connector
import requests

#Connect to MySql and Create DB if it doesn't exist
print('------------------------')
print('2.  Create Database')
from preview_extract import preview_extractor

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
  database=db
)

mycursor = mydb.cursor()
#=========================================
# DROP TABLES
#=========================================

print('------------------------')
print('2.  Drop tables')

print('1.  mlb_model Schema: Dropping Tables')
drop_cursor = mydb.cursor()

#order is important when dropping due to fk constraints
drop_cursor.execute('drop table if exists mlb_model.preview')
drop_cursor.execute('drop table if exists mlb_model.result')




#=========================================
# CREATE TABLES
#=========================================

print('------------------------')
print('3.  Creating tables')


#preview table
mycursor.execute \
("create table mlb_model.preview \
  (preview_id varchar(255)\
  ,game_no int \
  ,away_pitcher_rh boolean \
  ,away_pitcher_record float\
  ,away_pitcher_era float\
  ,away_pitcher_ip float\
  ,home_pitcher_rh boolean\
  ,home_pitcher_record float\
  ,home_pitcher_era float\
  ,home_pitcher_ip float\
  ,away_record float\
  ,away_last_ten float\
  ,away_venue_record float\
  ,away_pitcher_type_record float\
  ,home_record float\
  ,home_last_ten float\
  ,home_venue_record float\
  ,home_pitcher_type_record float\
  ,away_ops_vs_pitcher_type float\
  ,home_ops_vs_pitcher_type float\
  ,matchup_count integer\
  ,home_matchup_record float\
  ,primary key (preview_id))")


mycursor.execute \
("create table mlb_model.result \
  (result_id int(10) not null\
  ,home_name varchar(255)\
  ,home_score int(2) \
  ,away_name varchar(255) \
  ,away_score int(2)\
  ,home_win boolean\
  ,date varchar(255)\
  ,primary key (result_id))")

days=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
months=['05','06','07','08','09','10',]

for m in months:
  for d in days:
    try:
      home_abv='BAL'
      year='2018'
      month=m
      day=d




      url=f'https://www.baseball-reference.com/previews/{year}/{home_abv}{year}{month}{day}0.shtml'

      stat_list=list(preview_extractor(url,home_abv,year,month,day))
      string_list=[]
      for i in stat_list:
        string_list.append(str(i))
      # resulta=(1,"cubs",1,"bears",2,1,"20190101")
      # resultInsert="INSERT INTO result (result_id,home_name,home_score,away_name,away_score,home_win,date) VALUES (%s,%s,%s,%s,%s,%s,%s)"
      # mycursor.execute(resultInsert, resulta)

      previewInsert = "INSERT INTO preview (preview_id,game_no,away_pitcher_rh,away_pitcher_record,away_pitcher_era,away_pitcher_ip,home_pitcher_rh,home_pitcher_record,home_pitcher_era,home_pitcher_ip,away_record,away_last_ten,away_venue_record,away_pitcher_type_record,home_record,home_last_ten,home_venue_record,home_pitcher_type_record,away_ops_vs_pitcher_type,home_ops_vs_pitcher_type,matchup_count,home_matchup_record) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
      # away_venue_record,away_pitcher_type_record,home_record,home_last_ten,home_venue_record,home_pitcher_type_record,away_ops_vs_pitcher_type,home_ops_vs_pitcher_type,matchup_count,home_matchup_record

      mycursor.execute(previewInsert, string_list) 
      mydb.commit()
      preview_id=f'{home_abv}{year}{month}{day}'
      print (f'{preview_id} extract complete')
    except:
      print(f'date({day}) not found')
print('------------------------')
print('--- Job Completed ---')
