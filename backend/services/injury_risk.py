import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
from unidecode import unidecode
from services.all_nba_data import *
from services.all_nba_functions import *

def filter_career_stats_for_injury(input):
    return filter_stats(input, 'other')



def injury_risk(input):
    #nba_df = pd.read_csv('data/filtered-career-stats-for-injury.csv')
    nba_df = input
    new_df = pd.DataFrame()
    for id in id_list:
        name = nba_players_dict[id]
        player_df = nba_df[nba_df['Player'] == name]
        if len(player_df) > 2:
            player_df = player_df.tail(3)
        
        new_df = pd.concat([new_df, player_df], ignore_index= True)

    
    #new_df.to_csv('data/filtered-career-stats-3.csv', index= False)
    return new_df
        

def injury_risk_2(input):
    #nba_df = pd.read_csv('data/filtered-career-stats-3.csv')
    nba_df = input
    new_df = pd.DataFrame()

    for id in id_list:
        name = nba_players_dict[id]
        player_df = nba_df[nba_df['Player'] == name]
        avg_gms = 0
        count = 0
        for index,row in player_df.iterrows():
            if 'did' in str(row['G']).lower():
                count +=1
            elif float(row['G']) < 67:
                count+= 1
        
        if (len(player_df) == 3):
            val1 = player_df.iat[0,6]
            val2 = player_df.iat[1,6]
            val3 = player_df.iat[2,6]
            if 'did' in str(val1).lower():
                val1 = 0
            if 'did' in str(val2).lower():
                val2 = 0
            if 'did' in str(val3).lower():
                val3 = 0

            avg_gms = (float(val1)*0.1 + float(val2)*0.3 + float(val3)*0.6)
        elif (len(player_df) == 2):
            val1 = player_df.iat[0,6]
            val2 = player_df.iat[1,6]
            if 'did' in str(val1).lower():
                val1 = 0
            if 'did' in str(val2).lower():
                val2 = 0
            avg_gms = (float(val1)*0.3333 + float(val2)*0.6667)
        elif (len(player_df)==1):
            val1 = player_df.iat[0,6]
            if 'did' in str(val1).lower():
                val1 = 0
            avg_gms = float(val1)
        
        val = (82-avg_gms)/82 
        val = abs(round(val * (1.5*count),2))
        val2 = round(abs(val-4.5)/4.5,4)
        result_df = pd.DataFrame({'Player': [name], 'Injury Risk Value': [val], 'Scaled Injury Risk Value': [val2]})
        new_df = pd.concat([new_df, result_df], ignore_index= True)

    new_df = new_df.sort_values(by = 'Scaled Injury Risk Value', ascending= False)
    #new_df.to_csv('data/injury_risk.csv', index= False)
    return new_df
    