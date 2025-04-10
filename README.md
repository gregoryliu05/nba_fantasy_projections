## Overview 
This project aims to build an NBA player projection model that assesses player performance and predicts potential breakout candidates. By considering factors like player age, injuries, consistency, trade impacts, and development trends, the model will help provide a clearer outlook on whether a player is likely to outperform or regress in the upcoming season. Key statistical methods and algorithms, such as linear regression, K-means clustering, and decision tree regression, will be used to generate insights on player growth trajectories and value.

# Key Features 
Breakout Year Algorithm
For rookies and second-year players like Victor Wembanyama, our model will identify potential breakout candidates by evaluating:
- Top Performance Games: Using a player's best games to measure potential, rather than solely relying on season averages.
- Age and Surrounding Players: Factoring in a player’s situation, experience, and teammates to assess room for growth.

# Injury Analysis
Our model considers a player’s injury history and projected durability by:
Analyzing games missed in past seasons.
- Accounting for injury-prone players like Joel Embiid, who may be rated high for potential but discounted slightly for 
  availability risks.
- Sources such as social media updates (e.g., Adrian Wojnarowski’s Twitter) could provide real-time injury insights, although 
  their inclusion will depend on feasibility.

# Consistency Evaluation
To gauge consistency, we will measure:
- True Shooting Percentage (TS%) and Effective Field Goal Percentage (eFG%) variability.
- Shot Type Analysis: Free throws, rim attempts, and other high-efficiency shots will be examined to assess consistency over 
  time.
- Using game log data, we can track points, field goal percentage variance, and other metrics for an in-depth view of 
  performance consistency.

# Regression and Progression by Age
Our model includes an age-based analysis, predicting if players are likely to improve or regress based on:
- Historical Data: Calculating a general regression rate for players over specific ages (e.g., 31-33) based on past seasons.
- Injury-Prone Players: Factoring in age and previous injuries to assess if a player may be more prone to decline.

# Statistical Modeling Techniques
- Linear Regression: Used to predict growth trends from one year to the next, especially for younger players (e.g., first to 
  second year).
- K-Means Clustering: Groups players by similar statistical profiles, helping identify undervalued players and breakout 
  candidates.
- Decision Tree Regression: Helps pinpoint the age and metrics where NBA players tend to decline, providing a data-backed 
  approach to player progression.

# Usage Rate and Scoring Model
Using ESPN’s point system, the model evaluates player efficiency across key stats:
- Points, 3PM, FGA, FGM, FTA, FTM, rebounds, assists, steals, blocks, and turnovers.






















