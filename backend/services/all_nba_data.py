import pandas as pd
import numpy as np
from unidecode import unidecode


nba_df =pd.DataFrame()

nba_players_df = pd.read_csv('../../data/all-nba-players.csv')

nba_gamelog_df = pd.read_csv('../../data/nba-gamelogs.csv')

nba_career_stats_df = pd.read_csv('../../data/nba-career-stats-raw.csv')


nba_players_dict = dict()

for i in range(len(nba_players_df)):
    nba_players_dict[nba_players_df.iat[i,0]] = nba_players_df.iat[i,1] + ' ' + nba_players_df.iat[i,2]


id_list = list(nba_players_df["ID"])

names_list = list(nba_players_df["First Name"].str.lower() + ' ' + nba_players_df['Last Name'].str.lower())

def get_rookie_list():
     nba_df = pd.read_csv('../../data/filtered-career-stats.csv')
     rookie_id_list = []
     for id in id_list:
         name = nba_players_dict[id]
         player_df = nba_df[nba_df['Player'] == name]
         if (player_df.iat[0,1] == '2023-24'):
             rookie_id_list.append(id)
     return rookie_id_list

rookie_list = get_rookie_list()

teams = ['atl', 'bos', 'brk', 'cho', 'chi', 'cle' ,'dal', 'den', 'det', 'gsw',
         'hou', 'ind', 'lac', 'lal', 'mem', 'mia', 'mil', 'min', 'nop', 'nyk',
         'okc', 'orl', 'phi', 'pho', 'por', 'sac', 'sas', 'tor', 'uta', 'was']

stats = ['FG', 'FGA', "FG%",
         "3P", '3PA', '3P%',
         'FT', 'FTA', 'FT%',
         'ORB', 'TRB', 'AST',
         'STL', 'BLK', 'TOV', 'PF'
         ]


