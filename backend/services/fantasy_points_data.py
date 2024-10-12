import pandas as pd
import random
pd.set_option('display.max_columns', None)
import time
import numpy as np
from unidecode import unidecode
from services.all_nba_data import *

def get_all_fantasy_points_gamelog(input):
    #nba_df = pd.read_csv('data/nba-gamelogs.csv')
    nba_df = input
    
    for id in id_list:
        name = nba_players_dict[id]
        player_gamelog = nba_df[nba_df['Player'] == name].copy()  # Use nba_df here
        
        # Calculate fantasy points for each game
        fantasy_points = []
        for i in range(len(player_gamelog)):
            pts = player_gamelog.iat[i, 25]
            threes = player_gamelog.iat[i, 11]
            fga = player_gamelog.iat[i, 9]
            fgm = player_gamelog.iat[i, 8]
            fta = player_gamelog.iat[i, 15]
            ftm = player_gamelog.iat[i, 14]
            reb = player_gamelog.iat[i, 19]
            ast = player_gamelog.iat[i, 20]
            stl = player_gamelog.iat[i, 21]
            blk = player_gamelog.iat[i, 22]
            tov = player_gamelog.iat[i, 23]
            game_points = pts + threes + fga * -1 + fgm * 2 + fta * -1 + ftm + reb + ast * 2 + stl * 4 + blk * 4 + tov * -2
            fantasy_points.append(game_points)
        
        # Add the fantasy points for this player to the DataFrame
        nba_df.loc[nba_df['Player'] == name, 'Fantasy PTS'] = fantasy_points

    # Save the updated DataFrame back to the CSV file
    #nba_df.to_csv('data/nba-gamelogs.csv', index=False)
    print("fantasy points gamelog done")
    return nba_df


# get_all_fantasy_points_gamelog()

        


