import pandas as pd
from bs4 import BeautifulSoup
import requests

def results_extractor():

    # Read text file
    year = ['2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']
    for i in year:
        df = pd.read_csv(f'Data/GL{i}.TXT', header = None)

    # Function to create column for winning team
    def homeTeamWon(row):
        if row[10] > row[9]:
            return 1
        else:
            return 0

    # Add home team win/lose column
    df['HomeWin'] = df.apply(homeTeamWon)

    # Rename columns
    df.rename({0: 'Date', 1: 'GameNum', 3: 'Away Team', 9: 'Away Team Score',
            6: 'Home Team', 10: 'Home Team Score'}, axis=1, inplace=True)

    # Create new dataframe with only important columns
    df2 = df[['Date','GameNum','Away Team','Away Team Score','Home Team','Home Team Score','HomeWin']]

    df2 = df2.applymap(str)

    # Create an ID column
    df2['ID'] = df2['Home Team'] + df2['Date'] + df2['GameNum']

    # Reformat the dataframe
    results_table = df2[['ID', 'Date','GameNum','Home Team','Home Team Score','Away Team','Away Team Score','HomeWin']]
    return results_table