from services.all_nba_data import *
from services.all_nba_functions import * # done
from services.average_fpts import *
from services.consistency import * #done 
from services.fantasy_points_data import * # done
from services.final_data import *
from services.injury_risk import * #done 
from services.rookie_projections import * # done

def final_process():   
    # 1. get scraping data for both career and gamelog

    #career_stats_df = scrape_nba_players_averages() #all_nba_functions # now returns a dataframe
    career_stats_df = nba_career_stats_df
    #gamelog_df = scrape_nba_players_gamelog() # average_fpts # now returns a dataframe
    gamelog_df = nba_gamelog_df

    # 2. filter career stats for both injury risk and projections
        
    filtered_avgs_for_projections_df = filter_career_stats_for_projections(career_stats_df) #all_nba_functions   # done 

    # gets avg fpts for every season of every player's career
    filtered_avgs_for_projections_df = get_all_fantasy_points_filtered(filtered_avgs_for_projections_df) #all_nba_functions # done  

    # injury risk
    filtered_avgs_for_ir_df = filter_career_stats_for_injury(career_stats_df) # injury_risk #done 



    #3. get fantasy pts gamelog 

    # get fpts gamelog
    gamelog_df = get_all_fantasy_points_gamelog(gamelog_df) # fantasy_points_data #done 



    #4. get rookie projections

    rookie_id_list = get_rookie_list(filtered_avgs_for_projections_df) # rookie projections # done

    filtered_gamelog_rookies = get_all_rookies(gamelog_df, rookie_id_list) #rookie projections #done
    rookies_best_10_gamelog = avg_10_best_games(filtered_gamelog_rookies, rookie_id_list) #rookie projections #done

    #5. get injury risk values
    ir_df = injury_risk(filtered_avgs_for_ir_df) # injury_risk #done
    injury_risk_values_df = injury_risk_2(ir_df) #injury_risk #done



    #6. get consistency value

    # get total and avg fpts for each player from last szn
    total_and_avg_fpts_2024_df = get_all_fantasy_points(gamelog_df) #average_fpts #done 
        
        # get consistency value
    consistency_scores_df =nba_players_fantasy_pts_variance(total_and_avg_fpts_2024_df, career_stats_df, gamelog_df) # consistency #done 


    #7. get projections for all other players, then final data
    final_data(filtered_avgs_for_projections_df, consistency_scores_df, injury_risk_values_df, rookies_best_10_gamelog, rookie_id_list) 

    # change up the way we get projections, turn it into sql table???
        








