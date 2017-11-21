import os
from urllib.request import urlretrieve

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
        urlretrieve(URLS[year], fname)

    data = pd.read_csv(fname, parse_dates=True, dayfirst=True, index_col='Datum')

    # filter by location
    data = data[data.Standort == location]

    # subselect only the Velo data
    data = data[["Velo_in", "Velo_out"]]

    data['Total'] = data.Velo_in + data.Velo_out

    return data


def holidays():
    """Holidays in Zuerich"""
    return pd.read_csv("holidays.csv", parse_dates=True, index_col=0)
