import pandas as pd
from bs4 import BeautifulSoup
import requests

def results_extractor(year):

    # Read text file

        df = pd.read_csv(f'Data/GL{year}.TXT', header = None)

        # Add home team win/lose column
        df['HomeWin'] = ""
        df.loc[df[10]>df[9],['HomeWin']]='1'
        df.loc[df[9]>df[10],['HomeWin']]='0'

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

