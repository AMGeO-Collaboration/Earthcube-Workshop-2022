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

def polar2dial(ax):
    """
    Turns a matplotlib axes polar plot into a dial plot
    """
    #Rotate the plot so that noon is at the top and midnight
    #is at the bottom, and fix the labels so radial direction
    #is latitude and azimuthal direction is local time in hours
    ax.set_theta_zero_location('S')
    theta_label_values = np.array([0.,3.,6.,9.,12.,15.,18.,21.])*180./12
    theta_labels = ['%d' % (int(th/180.*12)) for th in theta_label_values.flatten().tolist()]
    ax.set_thetagrids(theta_label_values,labels=theta_labels)

    r_label_values = 90.-np.array([80.,70.,60.,50.,40.])
    r_labels = [r'$%d^{o}$' % (int(90.-rv)) for rv in r_label_values.flatten().tolist()]
    ax.set_rgrids(r_label_values,labels=r_labels)
    ax.set_rlim([0.,40.])
    
def plot_epot_map(fig, lats, lons, epot):
    """
    Plots basic AMGeO Electric potential map on a dial plot

    Ex:
        fig = plt.figure(figsize=(4, 4))
        epot = ds['epot'][idx]
        dt = epot.time.values
        ax = plot_epot_map(fig, epot.lat, epot.lon, epot)
    """
    ax = fig.add_subplot(111, projection='polar')
    polar2dial(ax)
    
    # plotting
    r = 90.-lats
    th = np.radians(lons)
    v = 30000
    levels=np.linspace(-v,v,30)
    cb = ax.contourf(th,r,epot,levels=levels,cmap='RdBu_r', vmin=-v, vmax=v,extend='both')
    
    # metadata attributes accessible on a DataArray
    units = epot.attrs['units']
    description = epot.attrs['longname']
    
    fig.colorbar(cb,label=f'{description} [{units}]')
    return ax