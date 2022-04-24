
#Imports
import pandas as pd
import numpy as np
import warnings
import datetime as dt 
from datetime import timedelta
warnings.filterwarnings("ignore")

#check that all these libs are existed in python_package in lambda layer you use.

# the below code is to clean, transform the fields and convert to df of excel files of pvn povider.
def cent_function(pvn):
    df_dict = pd.read_excel(pvn, sheet_name=None)
    df = pd.DataFrame()
    for i, x in df_dict.items():

        x['Unnamed: 0'] = x['Unnamed: 0'].replace({'Scheduled Departure ': 'Scheduled Departure',
                                              'DATE: ': 'DATE:'
                                              })
        index = x.index[x['Unnamed: 0'] == 'Scheduled Departure'].tolist()[0]
        drop_list = x.index[x['Unnamed: 0'] == 'Scheduled Departure'].tolist()
        x.columns = x.iloc[index]
        x.drop(drop_list, inplace=True)
        x.drop(x.index[x['Scheduled Departure'] == 'DATE:'].tolist(),inplace=True)
        x.drop(x.index[x['Scheduled Departure'].str.startswith('TRAVELING', na=False)].to_list(), inplace=True)
        x = x[~x['Actual Departure'].isnull()]
        x['Date'] = i
        df = df.append(x)
    df = df.reset_index().drop('index', axis=1)
    df['Date'] = df['Date'].str.replace('2709201','27092021')
    df['Date'] = pd.to_datetime(df['Date'], format= '%d%m%Y')
    df.drop('Comments', axis=1, inplace=True)
    df.drop('Total Passengers',axis=1, inplace=True)
    df.drop('Total Time Taken in Minutes', axis=1, inplace=True)

    #here is new commit
    df.rename(columns = {'No. of Passengers/ Departure':'PassengersAtDeparture'}, inplace = True)
    df.rename(columns = {'No. of Passengers / Arrival':'PassengerAtArrival'}, inplace = True)
    df.rename(columns = {'Time of Arrival Back At Station':'ActualArrival'}, inplace = True)
    df.rename(columns = {'Vehicle reg':'Vehicle'}, inplace = True)
    df.dropna(subset=['PassengersAtDeparture'],inplace=True)
    df['PassengersAtDeparture'] = df['PassengersAtDeparture'].astype(int)
    df['PassengerAtArrival'] = df['PassengerAtArrival'].astype(int)
    df.drop('Driver', axis=1, inplace=True)
    df['Association'] = 'Tshwane Taxi Association'
    df['Station'] = 'Centurion'


    def stations_name(RouteName):
        if RouteName == "MCS1":
           return 'Midstream'
        elif RouteName == "HCS1":
           return  'Highveld'
        if RouteName == "QHS1":
           return  'Queenswood'
           
    df['RouteName'] = df['RouteName'].apply(stations_name)
  
    return df

