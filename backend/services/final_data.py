import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
from unidecode import unidecode
from services.all_nba_data import *
import matplotlib.pyplot as plt
from scipy import stats
from statistics import linear_regression
from models import Player
from config import db

# INSTEAD OF CSV, MAYBE I COULD ADD EACH YR AS A ROW TO A SQL TABLE
def get_2_seasons_data(yr1, yr2, input_df):
    nba_df = input_df
    yr1_fpts = []
    yr2_fpts = []

    for id in id_list:
        name = nba_players_dict[id]
        player_gamelog = pd.DataFrame()
        player_gamelog = nba_df[nba_df['Player'] == name]
        
        if player_gamelog.empty:
            print(f"No data for player {name}")
            continue

        if len(player_gamelog) > yr1:
            yr1_fpts.append(player_gamelog.iat[yr1-1, player_gamelog.columns.get_loc('Avg FPTS')])
            yr2_fpts.append(player_gamelog.iat[yr2-1, player_gamelog.columns.get_loc('Avg FPTS')])
    test_df = pd.DataFrame({f'year = {yr1}': yr1_fpts, f'year = {yr2}': yr2_fpts})
    x = test_df[f'year = {yr1}'] 
    y = test_df[f'year = {yr2}'] 
    slope1, intercept = linear_regression(x,y, proportional= True)
    return slope1

def get_all_predictions(input_df):
    dictionary = dict()
    for i in range(16):
        data = get_2_seasons_data(i+1, i+2, input_df)
        dictionary[i+1] = data
    print(dictionary)
    return dictionary
        
def final_data(filtered_career_stats_df, consistency_df, injury_risk_df, rookies_best_games, rookie_id_list):
    # nba_df = pd.read_csv('data/filtered-career-stats.csv')
    # consistency_df = pd.read_csv('data/fantasy-pts.csv')
    # injury_risk_df = pd.read_csv('data/injury_risk.csv')
    # rookies_best_games = pd.read_csv('data/rookie-best-10-games-avg.csv')
    nba_df = filtered_career_stats_df
    consistency_df =consistency_df
    injury_risk_df = injury_risk_df
    rookies_best_games = rookies_best_games
    dictionary = get_all_predictions(filtered_career_stats_df)
    for id in id_list:
        name = nba_players_dict[id]
        player_df = nba_df[nba_df['Player'] == name]
        avg_fpts_row = consistency_df[consistency_df['Player'] == name]
        avg_fpts = avg_fpts_row['Avg FPTS'].values[0]
        projected_avg_fpts = 0
        yr = len(player_df)
        games_played = float(player_df.iloc[yr-1, 6])
        if id in rookie_id_list:
            best_games_avg = rookies_best_games[rookies_best_games['Player'] == name]
            best_games_avg = best_games_avg['Avg FPTS of Best 10'].values[0]
            projected_avg_fpts = round(avg_fpts*0.8 + best_games_avg *0.2, 2)
        else:
            projection_val = dictionary[min(yr,16)]
            projected_avg_fpts = round(avg_fpts * projection_val,2)

        consistency = consistency_df[consistency_df['Player'] == name]
        consistency = round(consistency['Consistency Score Scaled'].values[0],2)
        injury_risk = round(injury_risk_df[injury_risk_df['Player'] == name],2)
        injury_risk = injury_risk['Scaled Injury Risk Value'].values[0]
        consistency_injury_risk = round(consistency*(1/3) + injury_risk * (2/3),2)
        final_score = round((projected_avg_fpts + ((projected_avg_fpts * games_played)/67) 
                             + (projected_avg_fpts * (consistency_injury_risk)))/3,2)
        # Instead of saving to CSV, insert into the Player model (DB)
        player_in_db = Player.query.filter_by(player=name).first()

        # If the player exists, update their values
        if player_in_db:
            player_in_db.position = "Some Position"  # Adjust position if needed
            player_in_db.average_fpts = avg_fpts
            player_in_db.projected_fpts = projected_avg_fpts
            player_in_db.consistency = consistency
            player_in_db.injury_risk = injury_risk
            player_in_db.consistency_injury_risk = consistency_injury_risk
            player_in_db.overall_score = final_score
            #player_in_db.games_played = games_played
        else:
            # Create a new player if they don't exist in the database
            new_player = Player(player=name,
                                position="Some Position",  # Adjust the position as needed
                                average_fpts=avg_fpts,
                                projected_fpts=projected_avg_fpts,
                                consistency=consistency,
                                injury_risk=injury_risk,
                                consistency_injury_risk=consistency_injury_risk,
                                overall_score=final_score)
                                #games_played = games_played)
            db.session.add(new_player)
        
        # Commit changes to the database
        db.session.commit()

    print("Data successfully added to the database.")
