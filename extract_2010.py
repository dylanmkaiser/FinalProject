import pandas as pd
from bs4 import BeautifulSoup
import requests

#Function that calculates win % or returns 50% if no record
def record_split(record_string):
    cleaned=record_string.strip(',').split('-')
    if int(cleaned[0])+int(cleaned[1])==0:
        return 0
    else:
        return round(int(cleaned[0])/(int(cleaned[1])+int(cleaned[0])),2)


def extractor_2010(url,home_abv,year,month,day,gno):


    preview_id=f'{home_abv}{year}{month}{day}{gno}'

 


    #Scrape Pandas Tables
    tables=pd.read_html(url)

   
    #Scrape Soup
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Number of Games Played This Season/Test if We Should Record Data
    game_no_list=soup.find_all('tr')[0].find_all('td')[0].get_text().split()[1].strip(',').split('-')
    game_no=int(game_no_list[1])+int(game_no_list[0])
    
    #Away Pitcher Handedness
    away_pitcher_hand=soup.find_all('h3')[0].get_text().split('(')[1].split()[1]
    if away_pitcher_hand=='LHP,':
        away_pitcher_rh=0
    else: 
        away_pitcher_rh=1


    #Away Pitcher Record
    try:
        away_pitcher_record=record_split(soup.find_all('h3')[0].get_text().split('(')[1].split()[2].strip(','))
    except: 
        away_pitcher_record=0

    #Away Pitcher ERA
    try:
        away_pitcher_era=soup.find_all('h3')[0].get_text().split('(')[1].split()[3].strip(')')
    except:
        away_pitcher_era=0

    #Away Pitcher Innings Pitched, may contain prior year data if before May
    try:
        away_pitcher_ip=tables[1]['IP'][0]
    except:
        away_pitcher_ip=0

    #Home Pitcher Handedness
    home_pitcher_hand=soup.find_all('h3')[1].get_text().split('(')[1].split()[1]
    if home_pitcher_hand=='LHP,':
        home_pitcher_rh=0
    else: 
        home_pitcher_rh=1


    #Home Pitcher Record
    try:
        home_pitcher_record=record_split(soup.find_all('h3')[1].get_text().split('(')[1].split()[2].strip(','))
    except: 
        home_pitcher_record=0

    #Home Pitcher ERA
    try:
        home_pitcher_era=soup.find_all('h3')[1].get_text().split('(')[1].split()[3].strip(')')
    except:
        home_pitcher_era=0

    #Home Pitcher Innings Pitched, may contain prior year data if before May
    try:
        home_pitcher_ip=tables[2]['IP'][0]
    except:
        home_pitcher_ip=0

    #Away Team Overall Win/Loss Record
    away_record=record_split(soup.find_all('tr')[0].find_all('td')[0].get_text().split()[1].strip(','))


    #Away Team Win/Loss Record in Last 10 Games
    away_last_ten=record_split(soup.find_all('pre')[0].get_text().split('Last 10')[2].split(' ')[1])

    #Away Team Record as Away Team 
    away_venue_record=record_split(soup.find_all('pre')[0].get_text().split('Road')[0].split('   ')[1])

    #Away Team Record vs Home Team Pitcher Type
    if home_pitcher_rh==1:
        away_pitcher_type_record=record_split(soup.find_all('pre')[0].get_text().split('vsRHP:')[1].split('  ')[1])
    else:
        away_pitcher_type_record=record_split(soup.find_all('pre')[0].get_text().split('vsLHP:')[1].split('  ')[1])

    #Home Team Overall Win/Loss Record
    home_record=record_split(soup.findAll("span", {"class": "preview_teams"})[1].parent.text.split()[1].strip(','))

    #Home Team Win/Loss Record in Last 10 Games
    home_last_ten=record_split(soup.find_all('pre')[1].get_text().split('Last 10')[2].split(' ')[1])

    #Home Team Record as Home Team 
    home_venue_record=record_split(soup.find_all('pre')[1].get_text().split('Home:')[1].split('  ')[2])

    #Home Team Record vs Away Team Pitcher Type
    if away_pitcher_rh==1:
        home_pitcher_type_record=record_split(soup.find_all('pre')[1].get_text().split('vsRHP:')[1].split('  ')[1])
    else:
        home_pitcher_type_record=record_split(soup.find_all('pre')[1].get_text().split('vsLHP:')[1].split('  ')[1])

    #Away Team Ops vs Home Pitcher Type
    row=tables[6].loc[tables[6][0] == 'IP'].index[0]
    column=tables[6].loc[0,:].loc[tables[6].loc[0,:]=='vLH/RH'].index[0]

    if home_pitcher_rh==1:
        away_ops_vs_pitcher_type=tables[6].loc[row,column].split('/')[1]
    else:
        away_ops_vs_pitcher_type=tables[6].loc[row,column].split('/')[0]

    #Home Team Batting Table, may contain prior year data if before May
    row=tables[7].loc[tables[7][0] == 'IP'].index[0]
    column=tables[7].loc[0,:].loc[tables[7].loc[0,:]=='vLH/RH'].index[0]

    #Home Team Ops vs Away Pitcher Type
    if away_pitcher_rh==1:
        home_ops_vs_pitcher_type=tables[7].loc[row,column].split('/')[1]
    else:
        home_ops_vs_pitcher_type=tables[7].loc[row,column].split('/')[0]


    #Number of Matchups this Season
    try:
        #Who is the home team?
        home_team=soup.text.split('@ ')[1].split(',')[0]

        #Matchup record
        if soup.find_all('pre')[2].text.split(' - ')[1].split(' ')[0] == home_team:
            home_matchup_record=record_split(soup.find_all('pre')[2].text.split(' - ')[1].split(' ')[2].split()[0].strip(';'))
        else:
            home_matchup_record=1-record_split(soup.find_all('pre')[2].text.split(' - ')[1].split(' ')[2].split()[0].strip(';'))
            
        #How many matchups
        no_games_list=soup.find_all('pre')[2].text.split(' - ')[1].split(' ')[2].split(';')[0].split('-')
        matchup_count=int(no_games_list[1])+int(no_games_list[0])

    except:
        matchup_count=0
        home_matchup_record=.5

    preview_data=(preview_id,game_no,
    away_pitcher_rh,away_pitcher_record,away_pitcher_era,away_pitcher_ip,
    home_pitcher_rh,home_pitcher_record,home_pitcher_era,home_pitcher_ip,
    away_record,away_last_ten,away_venue_record,away_pitcher_type_record,
    home_record,home_last_ten,home_venue_record,home_pitcher_type_record,
    away_ops_vs_pitcher_type,home_ops_vs_pitcher_type,
    matchup_count,home_matchup_record)

    return(preview_data)






# home_abv='CLE'
# day='26'
# month='05'
# year='2010'
# gno='0'

# url=f'https://www.baseball-reference.com/previews/{year}/{home_abv}{year}{month}{day}{gno}.shtml'
# print(preview_extractor(url,home_abv,year,month,day,gno))


