### YOUR IMPORTS HERE ###
import numpy as np, pandas as pd, matplotlib as mp, seaborn as sns, plotly.express as px
def query_climate(df: pd.DataFrame, country: str, year_begin: int, year_end: int, month: int) -> pd.DataFrame:
    '''
    Description:
    This function takes in a dataframe filled with information about weather stations and outputs a dataframe
    with that info for a specific country, year interval, and specific month
    Arguments:
    Dataframe with all the globes weather data
    country, string; country we want to analyze
    year_begin, int; year we want our interval to start
    year_end, int; year we want our interval to end
    month, int; the month we want to look at
    Returns:
    dataframe with our filters applied
    '''
    dfNew = df.set_index(keys=["ID", "Year", "Country","LATITUDE","LONGITUDE","NAME"])
    dfNew = dfNew.stack( dropna = False)
    dfNew = dfNew.reset_index()
    dfNew = dfNew.rename(columns = {"level_6": "Month" , 0: "Temperature (C)"})
    dfNew["Month"] = dfNew["Month"].str[5:].astype(int)
    filteredDf = dfNew[(dfNew['Country'] == country) & (dfNew['Year'] >= year_begin) & (dfNew['Year'] <= year_end) & (dfNew['Month'] == month)]
    return filteredDf

def get_mean_temp(df: pd.DataFrame, country: str, year_begin: int, year_end: int, month: int) -> pd.DataFrame:
    '''
    Description:
    This function does the same thing as the above function, but also attaches a new column with the average temp for our specific month
    Arguments: 
    same arguments as the above function
    Returns:
    same as the above but with a new mean temp column
    '''
    df3 = query_climate(df=df, country=country, year_begin=year_begin, year_end=year_end, month=month)
    df4 = pd.DataFrame()
    df4['Mean Temp'] = df3.groupby(["ID", 'Month'])[["Temperature (C)"]].mean().round(2)
    df4 = df4.reset_index()
    df3['Mean Temp'] = df4['Mean Temp']
    df3 = pd.merge(df3, df4, on=["ID",'Month'])
    df3 = df3.drop(columns = ['Mean Temp_x'])
    df3 = df3.rename(columns={"Mean Temp_y": "Mean Temp"})
    return df3

def temperature_plot(df: pd.DataFrame, country: str, year_begin: int, year_end: int, month: int):
    '''
    Description: 
    This function plots our weather data as a scatter heat map so we can see the temperature variations at each weather station
    Arguments:
    Same arguments as the above functions
    Returns:
    Scatter heat map plot of our desired country with colored dots corresponding to the average temperature
    '''
    temp = 'Mean Temp'
    if year_begin == year_end:
        temp = 'Temperature (C)'
    fig = px.scatter_map(get_mean_temp(df=df, country=country, year_begin=year_begin, year_end=year_end, month=month),
                        lat="LATITUDE",
                        lon="LONGITUDE",
                        hover_name="NAME",
                        color=temp,
                        color_continuous_scale="plasma",
                        zoom=1,
                        height=300,
                        map_style="carto-positron")
  #  fig.suptitle(f"Average Temperature at each station during {year_begin} to {year_end} in Month {month}")
    if temp == 'Temperature (C)':
        fig.update_layout(title = {'text': f"Temperature at each station during {year_end} in Month {month}", 'font': {'size': 15} }, margin={"r": 0, "t": 20, "l": 0, "b": 0})
    else: 
        fig.update_layout(title = {'text': f"Average Temperature at each station during {year_begin} to {year_end} in Month {month}", 'font': {'size': 15} }, margin={"r": 0, "t": 25, "l": 0, "b": 0})
    
    return fig