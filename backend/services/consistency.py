import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
from unidecode import unidecode
from services.all_nba_data import *

def nba_players_fantasy_pts_variance(input, career_stats, gamelogs):
    epsilon = 1e-10  # A small number to prevent division by zero
    #fantasy_df = pd.read_csv('data/fantasy-pts.csv')
    fantasy_df = input
    for id in id_list:
        name = nba_players_dict[id]
        player_gamelog = gamelogs[(gamelogs['Player'] == name)].copy()
        player_gamelog['Fantasy PTS'] = pd.to_numeric(player_gamelog['Fantasy PTS'], errors='coerce')
        # Get games played and convert to numeric
        games_played = career_stats[(career_stats['Player'] == name) & (career_stats['Season'] == '2023-24')]['G']
        games_played = pd.to_numeric(games_played, errors='coerce').fillna(-1)
        
        # Get total fantasy points and convert to numeric
        total_fpts = fantasy_df[fantasy_df['Player'] == name]['Total FPTS']
        total_fpts = pd.to_numeric(total_fpts, errors='coerce').fillna(0)

        # Handle cases where there's no data
        if games_played.empty or total_fpts.empty:
            print(f"No data for player {name}")
            continue
        
        games_played = games_played.values[0]
        total_fpts = total_fpts.values[0]
        
        # Avoid division by zero or invalid division
        if games_played <= 0:
            avg_player_fpts = 0
        else:
            avg_player_fpts = total_fpts / games_played

        print(name)
        fpts_variance = 0
        count = 0
        var_below_mean = 0
        fpts_avg_below_mean = 0
        for i in range(len(player_gamelog)):
            if player_gamelog.iat[i,28] < avg_player_fpts:
                count += 1
                var_below_mean += (player_gamelog.iat[i,28] - avg_player_fpts) ** 2
                fpts_avg_below_mean += player_gamelog.iat[i,28]
            fpts_variance += (player_gamelog.iat[i,28] - avg_player_fpts) ** 2
        
        fpts_variance = fpts_variance/(len(player_gamelog)-1)
        fpts_variance = round(fpts_variance,2)
        var_below_mean = round(var_below_mean/max(count-1,1),2)
        sd_below_mean = round(np.sqrt(var_below_mean),2)
        sd = round(np.sqrt(fpts_variance),2)
        if (sd + (sd_below_mean / max(fpts_avg_below_mean, epsilon)) * (count / max(games_played, epsilon))) != 0:
            consistency = round(avg_player_fpts / (sd + (sd_below_mean / max(fpts_avg_below_mean, epsilon)) * (count / max(games_played, epsilon))), 2)
        else:
            consistency = None  # or set a default value like 0, depending on your requirements
        if (count >0):
            fpts_avg_below_mean = round(fpts_avg_below_mean/count,2)
        
        consistency = consistency if consistency is not None else 0
        fantasy_df.loc[fantasy_df['Player'] == name, 'Consistency Score'] = consistency
        fantasy_df.loc[fantasy_df['Player'] == name, 'Consistency Score Scaled'] = round(consistency/4,3)

    fantasy_df =fantasy_df.sort_values(by= 'Avg FPTS', ascending= False)
    #fantasy_df.to_csv('data/fantasy-pts.csv', index= False)
    return fantasy_df