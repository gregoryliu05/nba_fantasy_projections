import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
from unidecode import unidecode
from services.all_nba_data import *


# def fantasy_pts_gamelog():
#     nba_df = pd.read_csv('data/nba-gamelogs.csv')
#     new_df = pd.DataFrame()
    
#     for id in id_list:
#         name = nba_players_dict[id]
        
#         # Filter the data for the player
#         player_df = nba_df[nba_df['Player'] == name].copy()
        
#         if player_df.empty:
#             print(f"No data found for player: {name}")
#             continue
        
#         # Select only relevant columns

        
#         # Sort by 'Fantasy PTS' and get the top 10 games
#         player_df = player_df.nlargest(10, 'Fantasy PTS')
        
#         # Concatenate the result to the new DataFrame
#         new_df = pd.concat([new_df, player_df], ignore_index=True)
    
#     # Save the result to a new CSV file
#     if not new_df.empty:
#         new_df.to_csv('data/fantasy-pts-gamelog.csv', index=False)
#         print("Data saved successfully.")
#     else:
#         print("No data to save.")

def get_rookie_list(career_stats):
    #nba_df = pd.read_csv('data/filtered-career-stats.csv')
    nba_df = career_stats
    rookie_id_list = []
    for id in id_list:
        name = nba_players_dict[id]
        player_df = nba_df[nba_df['Player'] == name]
        if (player_df.iat[0,1] == '2023-24'):
            rookie_id_list.append(id)
    print("rookie id list done")
    return rookie_id_list


def get_all_rookies(input, rookie_id_list):
    #gamelog_df = pd.read_csv('data/nba-gamelogs.csv')
    gamelog_df = input
    gamelog_df = gamelog_df[['Player', 'G', 'Date', 'Fantasy PTS']]
    new_df = pd.DataFrame()
    for id1 in rookie_id_list:
        name = nba_players_dict[id1]
        player_df1 = gamelog_df[gamelog_df['Player'] == name]
        #print(player_df1['Fantasy PTS'].dtype)
        player_df1.loc[:, 'Fantasy PTS'] = pd.to_numeric(player_df1['Fantasy PTS'], errors='coerce')
        #print(player_df1['Fantasy PTS'].unique())
        #print(player_df1[player_df1['Fantasy PTS'].isna()])

        # Now you can safely apply the nlargest() method
        if len(player_df1) >= 10:
            player_df1 = player_df1.nlargest(10, 'Fantasy PTS')
            print(name, player_df1['Fantasy PTS'].dtype)
        else:
            print(f"Not enough data to apply nlargest() for player {name}. Skipping.")
        new_df = pd.concat([new_df, player_df1], ignore_index=True)

    #new_df.to_csv('../../data/filtered-fantasy-pts-gamelog-rookies.csv', index= False)
    return new_df

#print(get_all_rookies(nba_gamelog_df,rookie_list))

def avg_10_best_games(input, rookie_id_list):
    #nba_df = pd.read_csv('data/filtered-fantasy-pts-gamelog-rookies.csv')
    nba_df = input
    new_df = pd.DataFrame()
    for id in rookie_id_list:
        name = nba_players_dict[id]
        player_df = nba_df[nba_df['Player'] == name]
        total = 0
        for index, row in player_df.iterrows():
            total += float(row['Fantasy PTS'])
        avg = total/10
        new_player_df = pd.DataFrame({'Player': [name], 'Avg FPTS of Best 10': [avg]})
        new_df = pd.concat([new_df, new_player_df], ignore_index= True)
    
    new_df = new_df.sort_values(by= 'Avg FPTS of Best 10', ascending= False)
    #new_df.to_csv('data/rookie-best-10-games-avg.csv', index= False)
    return new_df