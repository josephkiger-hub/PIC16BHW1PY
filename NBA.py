### YOUR IMPORTS HERE ###
import pandas as pd
def read_NBA_stats(url: str) -> pd.DataFrame:
    '''
    Description: 
    This method takes in a url of a csv file with a bunch of nba data
    and outputs a dataframe with more specific features
    Arguments:
    url string
    Returns:
    Dataframe with the year/season, player name, team, and the stats [Games played, points, rebounds, assist, steal, block] for that season
    '''
    df = pd.read_csv(url)
    newDf = df[['year','PLAYER','TEAM','GP','PTS','REB','AST','STL','BLK']]
    return newDf

def convert_to_averages(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Description:
    Takes in a dataframe that's been processed by read_NBA_stats and converts all the stats to season averages
    Arguments:
    Dataframe that has been processed
    Returns:
    new dataframe with computed averages
    '''
    newDf = df.copy()
    newDf['PTS'] = (df['PTS']/df['GP']).round(1)
    newDf['REB'] = (df['REB']/df['GP']).round(1)
    newDf['AST'] = (df['AST']/df['GP']).round(1)
    newDf['STL'] = (df['STL']/df['GP']).round(1)
    newDf['BLK'] = (df['BLK']/df['GP']).round(1)
    return newDf

def player_stat(df: pd.DataFrame, player: str, season: str, stat: str) -> pd.DataFrame:
    '''
    Description:
    This function takes in a data frame, a player name, the desired season, and a stat then outputs a one row dataframe
    with that information and the value of the stat for that season
    Arguments:
    Dataframe that has been processed
    Player name that is a string
    season that is a string 'YYYY-YY'
    stat string
    Returns:
    A new one row dataframe with the player and his desired stat for that season
    '''
    newDf = pd.DataFrame({
    'year': df['year'],
    'PLAYER': df['PLAYER'],
    'TEAM': df['TEAM'],
    'stat': stat,
    'value': df[stat]
    })
    newDf = newDf[(newDf['PLAYER'] == player) & (newDf['year'] == season)]
    newDf = newDf.reset_index()
    newDf = newDf.drop(columns = ['index'])
    return newDf

def leader(df: pd.DataFrame, season: str) -> pd.DataFrame:
    '''
    Description:
    This function creates a dataframe of the season leaders for all the different stats
    Arguments:
    Dataframe of the sesason's nba players with their stats
    Returns:
    Dataframe with the season leaders for each stat
    '''
    stat = 'GP'
    newDf = df[df['year'] == season]
    newDf = newDf.sort_values(by = stat, ascending = False)
    statCols = ['PTS','REB','AST','STL','BLK']
    leaderDf = player_stat(newDf, player = newDf['PLAYER'].iloc[0], season = season, stat = stat)
    for col in statCols:
        newDf = newDf.sort_values(by = col, ascending = False)
        leaderDf = pd.concat([leaderDf, player_stat(newDf, player = newDf['PLAYER'].iloc[0], season = season, stat = col)], ignore_index=True)
    leaderDf = leaderDf.head(6)
    return leaderDf