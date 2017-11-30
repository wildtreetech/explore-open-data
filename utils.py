import os
import urllib
import requests

import pandas as pd


def get_velo_data(location, year=2016):
    BASE = "https://data.stadt-zuerich.ch/dataset/verkehrszaehlungen_werte_fussgaenger_velo/resource/"
    URLS = {
        2016: BASE + "ed354dde-c0f9-43b3-b05b-08c5f4c3f65a/download/2016verkehrszaehlungenwertefussgaengervelo.csv",
        2015: BASE + "5c994056-eda6-48c5-8e61-28e96bcd04a3/download/2015verkehrszaehlungenwertefussgaengervelo.csv",
        2014: BASE + "bd2c9dd9-5b05-4303-a4c9-4a9f5b73e8f7/download/2014verkehrszaehlungenwertefussgaengervelo.csv",
        }

    if year not in URLS:
        raise ValueError("Year has to be one of 2014, 2015, 2016 "
                         "not %s." % year)

    fname = "bikes-%i.csv" % year
    if not os.path.exists(fname):
        with requests.get(URLS[year], stream=True, verify=False) as r:
            r.raise_for_status()
            with open(fname, 'wb') as w:
                for chunk in r.iter_content(chunk_size=65535):
                    w.write(chunk)

    data = pd.read_csv(fname, parse_dates=True, dayfirst=True, index_col='Datum')

    # filter by location
    data = data[data.Standort == location]

    # subselect only the Velo data
    data = data[["Velo_in", "Velo_out"]]

    data['Total'] = data.Velo_in + data.Velo_out

    return data


def get_weather_data():
    """Zurich weather data for 2016"""
    fname = 'weather-2016.html'
    if not os.path.exists(fname):
        data = ('messw_beg=01.01.2016&messw_end=31.12.2016&'
                'felder[]=Temp2m&felder[]=TempWasser&felder[]=Windchill&'
                'felder[]=LuftdruckQFE&felder[]=Regen&felder[]=Taupunkt&'
                'felder[]=Strahlung&felder[]=Feuchte&felder[]=Pegel&'
                'auswahl=2&combilog=mythenquai&suchen=Werte anzeigen')
        data = data.encode('ascii')

        req = urllib.request.Request(
            'https://www.tecson-data.ch/zurich/mythenquai/uebersicht/messwerte.php',
            method='POST',
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded",
                     'User-Agent': 'http://github.com/wildtreetech/explore-open-data'
                     },
            )

        with urllib.request.urlopen(req) as web:
            with open(fname, 'w') as local:
                local.write(web.read().decode('iso-8859-1'))

    df = pd.read_html(fname, attrs={'border': '1'}, skiprows=1)
    # take the first data frame from the list of data frames
    df = df[0]
    # this refers to the first column of the data frame now
    df[0] = pd.to_datetime(df[0], dayfirst=True)
    df.columns = ['Date', 'Temp', 'WaterTemp', 'Windchill', 'Pressure', 'Rain',
                  'Dewpoint', 'Radiation', 'Humidity', 'Waterlevel']
    df = df.set_index('Date')

    return df
