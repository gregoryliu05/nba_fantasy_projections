import pandas as pd
import random
pd.set_option('display.max_columns', None)
import time
import numpy as np
from unidecode import unidecode
from services.all_nba_data import *
from urllib.parse import quote


def scrape_nba_players_averages():
    nba_df = pd.DataFrame()

    for id in id_list:
        url = f'https://www.basketball-reference.com/players/{id}.html'
        print(f"Processing URL: {url}")
        url = quote(url, safe=':/')  # Encode the URL properly
    
        try:
            tables = pd.read_html(url, header=0, attrs={'id': 'per_game'})
            if len(tables) > 0:
                player_df = tables[0]
                player_df = player_df.drop(columns=['Awards'])
                player_df = player_df.dropna(how='all')
                player_df.insert(loc=0, column="Player", value=nba_players_dict[id])
                if not player_df.empty:
                    nba_df = pd.concat([nba_df, player_df], ignore_index=True)
                else:
                    print(f"Empty data for player ID {id}")

            else:
                print(f"No table found for player ID {id}")
        except Exception as e:
            print(f"Error processing {url}: {e}")
            continue

            # Debugging print statements
        print("Sleeping for a random time between 5 to 6 seconds...")
        time.sleep(random.randint(5,6))
        print("Continuing to the next request...")

    # Save to CSV
    if not nba_df.empty:
        #nba_df.to_csv('data/nba-career-stats-raw.csv', index=False)
        return nba_df
    else:
        print("No data collected, CSV will be empty.")


def filter_career_stats_for_projections(input):
    #filter_stats('data/nba-career-stats-raw.csv', 'data/filtered-career-stats.csv', 'Did Not Play')
    return filter_stats(input, "Did Not Play")


def get_all_fantasy_points_filtered(input):
    #nba_df = pd.read_csv('data/filtered-career-stats.csv')
    nba_df = input
    all_fpts_avg = []

    for id in id_list:
        name = nba_players_dict[id]
        player_gamelog = nba_df[nba_df['Player'] == name]
        
        if player_gamelog.empty:
            print(f"No data for player {name}")
            continue
        
        for i in range(len(player_gamelog)):
            # Check if the player did not play
            if isinstance(player_gamelog.iat[i, 29], str) and "Did Not Play" in player_gamelog.iat[i, 29]:
                print('Did not Play')
                game_points = 0
            else:
                pts = float(player_gamelog['PTS'].iloc[i])
                threes = float(player_gamelog['3P'].iloc[i])
                fga = float(player_gamelog['FGA'].iloc[i])
                fgm = float(player_gamelog['FG'].iloc[i])
                fta = float(player_gamelog['FTA'].iloc[i])
                ftm = float(player_gamelog['FT'].iloc[i])
                reb = float(player_gamelog['TRB'].iloc[i])
                ast = float(player_gamelog['AST'].iloc[i])
                stl = float(player_gamelog['STL'].iloc[i])
                blk = float(player_gamelog['BLK'].iloc[i])
                tov = float(player_gamelog['TOV'].iloc[i])
                game_points = pts + threes + fga * -1 + fgm * 2 + fta * -1 + ftm + reb + ast * 2 + stl * 4 + blk * 4 + tov * -2
                game_points = round(game_points, 2)
                print(f'{name}: {player_gamelog.iat[i,1]}')
            # Append the calculated points (or 0 if "Did Not Play") to the list
            all_fpts_avg.append(game_points)

    
    nba_df['Avg FPTS'] = all_fpts_avg
    #nba_df.to_csv('data/filtered-career-stats.csv', index=False)
    return nba_df
    


def filter_stats(input, additional_filter=None):
    #nba_df = pd.read_csv(input_file)
    nba_df = input

    # Initialize an empty list to collect indices to drop
    indices_to_drop = []

    # Iterate over the DataFrame
    for index, row in nba_df.iterrows():
        if row['Tm'] == 'TOT':
            season = row['Season']
            # Mark the next two rows for deletion, if they exist
            if nba_df.iat[index + 3, 1] == season:
                indices_to_drop.extend([index + 1, index + 2, index + 3])
            else:
                indices_to_drop.extend([index + 1, index + 2])
        if row['Season'] == 'Career':
            indices_to_drop.extend([index])
        if np.isnan(row['Age']):
            indices_to_drop.extend([index])

    # Filter out the indices that are beyond the DataFrame's length
    indices_to_drop = [i for i in indices_to_drop if i < len(nba_df)]
     # Apply any additional filters if provided
    if additional_filter:
        nba_df = nba_df[~nba_df["Pos"].str.contains(additional_filter, na=False)]

    # Drop the rows
    nba_df = nba_df.drop(indices_to_drop)

    # Optionally drop unnecessary columns (you can uncomment this if needed)
    # nba_df = nba_df.drop(columns='Unnamed: 31')

    # Save the result to a new CSV file
    #nba_df.to_csv(output_file, index=False)
    return nba_df















