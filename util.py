import pandas as pd
import numpy as np
from datetime import datetime
from apexpy import Apex

def read_amp_Itot_dat(amp_Itot_fn):
    """
    Reads an ampere 'dat' file into a pandas Dataframe 

    Ex: 
        `df_amp = read_amp_Itot_dat('path/to/amp_itot_daily_YYYYMMDD.dat')`
    """
    amp_Itot_names = ['year',
                'month',
                'day',
                'hour',
                'minute',
                'second',
                'I total up North [MA]', 
                'I total down North [MA]', 
                'I day up North [MA]', 
                'I day down North [MA]', 
                'I night up North [MA]', 
                'I night down North [MA]', 
                'I total up South [MA]', 
                'I total down South [MA]', 
                'I day up South [MA]', 
                'I day down South [MA]', 
                'I night up South [MA]', 
                'I night down South [MA]']
    df_amp = pd.read_csv(amp_Itot_fn,sep='\s+',names=amp_Itot_names,skiprows=1)
    df_amp['time']=pd.to_datetime(df_amp[['year','month','day','hour','minute','second']])
    df_amp.set_index('time',inplace=True)
    return df_amp

def datetime64_to_datetime(dt64):
    """Convert a numpy.datetime64 
    (time format used by Pandas/Xarray) 
    to a Python datetime.datetime
    (format expected by Apexpy)

    Can pass either an iterable object or single dt64
    """
    if hasattr(dt64, '__iter__'):
        return [el.astype('M8[ms]').astype('O') for el in dt64]
    else:
        return dt64.astype('M8[ms]').astype('O')

def get_amgeo_geodetic_coords(amgeo_lat, amgeo_lon, dt: datetime):
    """
    Get the geodetic coordinates of an AMGeO map at a specific time

    Returns
    ---
    geo_lat: ndarray
        24x37 array of geodetic latitude coords
    geo_lon: ndarray
        24x37 array of geodetic longitude coords

    Ex: 
        dt = datetime64_to_datetime(ds.time[0])
        amgeo_lat, amgeo_lon = ds.lat.values, ds.lon.values
        geo_lat, geo_lon = get_amgeo_geodetic_coords(amgeo_lat, amgeo_lon, dt)
    """
    amgeo_lats, amgeo_lons = np.zeros((24, 37)), np.zeros((24, 37))
    for i in range(24):
        for j in range(37):
            amgeo_lats[i][j] = amgeo_lat[i]
            amgeo_lons[i][j] = amgeo_lon[j]
    amgeo_lats, amgeo_lons = np.array(amgeo_lats), np.array(amgeo_lons)
    mlt = amgeo_lons / 180 * 12
    apex_out = Apex()
    geo_lat, geo_lon = apex_out.convert(amgeo_lats, mlt, 'mlt', 'geo', datetime=dt, height=110)
    return geo_lat, geo_lon