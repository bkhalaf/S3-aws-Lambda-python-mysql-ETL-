#Imports
import pandas as pd
import numpy as np
import warnings
import datetime as dt 
from datetime import timedelta
warnings.filterwarnings("ignore")

def alex_function(ats):
    df_dict = pd.read_excel(ats, sheet_name=None)
    sheets = []
    for i in df_dict:
        if ('2019' not in i) and ("ADMIN Page" not in i):
            sheets.append(i)
    df_dict = pd.read_excel(ats, sheet_name=sheets)
    df = pd.DataFrame()
    droplist = ['Unnamed: 15']
    for i,x in df_dict.items():
        x.rename(columns={'Actual Arrival': 'ActualArrival', 'Passengers Departure': 'PassengersAtDeparture',
                      'Passengers Arrival': 'PassengerAtArrival', 'Unnamed: 12':'ActualArrival',
                     'Unnamed: 13':'PassengersAtDeparture','Unnamed: 14':'PassengerAtArrival',
                         'Trip Type': 'TripType', 'Route Name':'RouteName','Scheduled Departure':'ScheduledDeparture',
                         'Actual Departure':'ActualDeparture'}, inplace=True)
        x = x.drop([t for t in droplist if t in x.columns], axis=1)
        x['Date'] = i
        x['RouteId'] = 36
        df = df.append(x)
    df = df.reset_index().drop('index', axis=1)
    df['Date']= df['Date'].replace({'20109':'2019', 'JANAUARY': 'JANUARY'}, regex=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Vehicle'] = df['Vehicle'].str.strip().str.replace(' ', '')
    df = df.dropna(subset=['StationId'])
    df = df.dropna(subset=['Vehicle'])
    df['TripType'] = df['TripType'].fillna('SHS')
    df['DepartureStatusText'] = df['DepartureStatusText'].fillna('on time')
    df['DepartureStatusText'] = df['DepartureStatusText'].replace({'On':'on'}, regex=True)
    df.rename(columns = {'DepartureStatusText':'DepartureStatus'}, inplace = True)
    df['Vehicle'] = df['Vehicle'].replace({';':''}, regex=True)
    df['Vehicle'] = df['Vehicle'].replace({'HD03HW':'HD03HWGP'}, regex=False)
    df = df.dropna()
    df = df.reset_index().drop('index', axis=1)
    df = df[~df['Vehicle'].isin(['NOCALL', 'NOTRIP','SERVICE '])]
    df = df[~df['ActualArrival'].isin(['NO CALL'])]
    df = df[~df['PassengersAtDeparture'].isin(['SERVICE ', 'due  to ', 'TRAFFIC', 'CANCELLED DUE TO PROTEST', 'CANCELLED DUE TO TRUFFIC',
                                              'CANCELLED DUE TO TRAFFIC', 'DUR TO PROTEST', 'DUE TO GAUTRAIN TO POWER'])]
    df['PassengersAtDeparture'] = df['PassengersAtDeparture'].astype(int)
    df['PassengerAtArrival'] = df['PassengerAtArrival'].astype(int)
    df['Association'] = "Alex Taxi Association"
    
    return df

