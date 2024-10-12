import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
from unidecode import unidecode
from services.all_nba_data import *
from services.all_nba_functions import *


def scrape_nba_players_gamelog(years=[2024]):
    nba_df = pd.DataFrame()  # Initialize nba_df as an empty DataFrame
    for y in years:
        for id in id_list:
            url = f'https://www.basketball-reference.com/players/{id}/gamelog/{y}'
            print(f"Processing URL: {url}")
            url = quote(url, safe=':/')  # Encode the URL properly
    
            try:
                tables = pd.read_html(url, header=0, attrs={'id': 'pgl_basic'})
                if len(tables) > 0:
                    player_df = tables[0]
                    player_df = player_df.drop(columns=['Rk', 'Unnamed: 5', 'Unnamed: 7'])
                    player_df = player_df[(player_df["AST"] != "Inactive") &  (player_df["AST"] != "Did Not Dress") & (player_df["AST"] != 'AST') & (player_df["AST"] != "Did Not Play") & (player_df["AST"] != "Not With Team") & (player_df["AST"] != "Player Suspended")]
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
        # nba_df.to_csv('data/nba-gamelogs.csv', index=False)
        return nba_df
    else:
        print("No data collected, CSV will be empty.")


def get_all_fantasy_points(input):
    nba_gamelog = input
    nba_df = pd.DataFrame()
    for id in id_list:
        name = nba_players_dict[id]
        player_gamelog = nba_gamelog[(nba_gamelog['Player'] == name)]
        fantasy_points = 0
        for i in range(len(player_gamelog)):
            pts = player_gamelog['PTS'].iloc[i]
            threes = player_gamelog['3P'].iloc[i]
            fga = player_gamelog['FGA'].iloc[i]
            fgm = player_gamelog['FG'].iloc[i]
            fta = player_gamelog['FTA'].iloc[i]
            ftm = player_gamelog['FT'].iloc[i]
            reb = player_gamelog['TRB'].iloc[i]
            ast = player_gamelog['AST'].iloc[i]
            stl = player_gamelog['STL'].iloc[i]
            blk = player_gamelog['BLK'].iloc[i]
            tov = player_gamelog['TOV'].iloc[i]
            game_points = pts + threes + fga*-1 + fgm *2 + fta *-1 + ftm + reb + ast *2 + stl * 4 + blk * 4 + tov *-2
            fantasy_points += int(game_points)
        avg_fpts = round(fantasy_points/(max(len(player_gamelog),1)),2)
        df = pd.DataFrame({
            'Player': [name],
            'Total FPTS' : [fantasy_points],
            'Avg FPTS' : [avg_fpts]
            })
        nba_df = pd.concat([nba_df, df], ignore_index= True)
    nba_df = nba_df.sort_values(by = 'Total FPTS', ascending= False)
    #nba_df.to_csv('data/fantasy-pts2.csv', index= False)
    return nba_df
