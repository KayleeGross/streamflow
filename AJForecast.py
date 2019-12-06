from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from matplotlib.figure import figaspect
from netCDF4 import Dataset
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime, timedelta
import os
import requests
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import netCDF4 as nc
import json
import io
import os


# file paths from swagger ui
url_a = 'http://10.200.28.72/api/v1/cnrfc?start_date=2018-10-1&end_date=2019-7-30&station=NDPC1&variable=exceedance90'
url_b = 'http://10.200.28.72/api/v1/cnrfc?start_date=2018-10-1&end_date=2019-7-30&station=NDPC1&variable=exceedance50'
url_c = 'http://10.200.28.72/api/v1/cnrfc?start_date=2018-10-1&end_date=2019-7-30&station=NDPC1&variable=exceedance10'
url_d = 'http://10.200.28.72/api/v1/cnrfc?start_date=2018-10-01&end_date=2019-07-30&variable=aj_raw_obs'

# file paths from openstack
url_1 = 'http://arsidboi1snowc1:8080/v1/AUTH_24a46c0130aa4d46a1f52a2aaff35fc3/forecast_data/DP_precip_thru0625.csv'
url_2 = 'http://arsidboi1snowc1:8080/v1/AUTH_24a46c0130aa4d46a1f52a2aaff35fc3/forecast_data/revised_swi.csv'
url_3 = 'http://arsidboi1snowc1:8080/v1/AUTH_24a46c0130aa4d46a1f52a2aaff35fc3/forecast_data/swe_ytd_swi.csv'
url_4 = 'http://arsidboi1snowc1:8080/v1/AUTH_24a46c0130aa4d46a1f52a2aaff35fc3/forecast_data/swe_ytd_runoff.csv'

# request files from swagger ui
r = requests.get(url_d).json()
df_runoff = pd.DataFrame(r['cnrfc'], columns=['date', 'aj_raw_obs'])
df_runoff['aj_raw_obs'] = df_runoff['aj_raw_obs'].rolling(5).mean()

r = requests.get(url_a).json()
df_forecast_90 = pd.DataFrame(r['cnrfc'], columns=['date', 'exceedance90'])

r = requests.get(url_b).json()
df_forecast_50 = pd.DataFrame(r['cnrfc'], columns=['date', 'exceedance50'])

r = requests.get(url_c).json()
df_forecast_10 = pd.DataFrame(r['cnrfc'], columns=['date', 'exceedance10'])

# merge files
df_forecast = pd.merge(df_forecast_90, df_forecast_50, on= 'date', how ='inner')
df_forecasts = pd.merge(df_forecast, df_forecast_10, on= 'date', how = 'inner')

# convert TAF to AF
x = 1000

# make new columns and set equal to old
df_forecasts['90'] = df_forecasts['exceedance90']*x
df_forecasts['10'] = df_forecasts['exceedance10']*x
df_forecasts['50'] = df_forecasts['exceedance50']*x
df_runoff['aj_raw_obs'] = df_runoff['aj_raw_obs']*x

# drop old columns
dfnew = df_forecasts.drop(columns=['exceedance90', 'exceedance50', 'exceedance10'])

# set index_col for data frames
dfnew.set_index(pd.to_datetime(dfnew['date']), inplace=True)
df_runoff.set_index(pd.to_datetime(df_runoff['date']), inplace=True)


# request files from openstack
r = requests.get(url_1).content
df_ppt = pd.read_csv(io.StringIO(r.decode('utf-8')), index_col=0, parse_dates=[0])

r = requests.get(url_2).content
df_revised_swi = pd.read_csv(io.StringIO(r.decode('utf-8')), index_col=0, parse_dates=[0])

r = requests.get(url_3).content
df_swe_swi = pd.read_csv(io.StringIO(r.decode('utf-8')), index_col=0, parse_dates=[0])

r = requests.get(url_4).content
df_swe_runoff = pd.read_csv(io.StringIO(r.decode('utf-8')),index_col=0, parse_dates=[0])


# create figure
fig1 = plt.figure(figsize=(9.85, 7), dpi=150)
ax = fig1.add_subplot(111)
ax2 = ax.twinx()

# plot forecast data
ax.plot(dfnew.index, dfnew['90'], 'salmon', label='exceedance90')
ax.plot(dfnew.index,dfnew['50'], 'powderblue', label='exceedance50')
ax.plot(dfnew.index,dfnew['10'], 'yellowgreen', label='exceedance10')
ax.plot(df_runoff.index, df_runoff['aj_raw_obs'], 'midnightblue', label='Cumulative Runoff')

# plot swi and swe
ax.plot(df_swe_swi.index, df_swe_swi['AF'], 'mediumpurple', label='Cumulative SWI+SWE')
ax.plot(df_swe_runoff.index, df_swe_runoff['current_swe_ytd_runoff'], 'darkgoldenrod', label='Cumulative Runoff+SWE')
ax.plot(df_revised_swi.index, df_revised_swi['normalized swi (AF)'], 'slategrey', label='Cumulative SWI')

# plot rainfall
ax2.bar(df_ppt.index, df_ppt["precip_in"].values, width=1,color='firebrick', label='Don Pedro Rainfall')
ax2.xaxis_date()

# set axis labels and ticks
ax.set_title('Tuolumne River Forecasts of April through July Runoff (AF)', fontsize=10, loc= 'center')
ax.set_xlabel('Date of Probabilistic Start', fontsize=10);
ax.set_ylabel('April through July Runoff (Acre-Feet)', fontsize=10);
ax2.set_ylabel('Rainfall [in.]', rotation=-90, fontsize=10)
ax2.yaxis.set_label_coords(1.07, 0.5)
ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
ax.set_yticks(125000+np.arange(0, 2625000, step=125000))
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))

# set params
ax.tick_params(axis='x', which='minor', bottom=False)
ax.tick_params('x', rotation=-90, labelsize=7)
ax.tick_params('y', labelsize=7)
ax2.tick_params('y', labelsize=7)
ax.grid(linewidth=0.5, alpha=0.5)
ax.set_xlim(pd.Timestamp('2018-10-01'), pd.Timestamp('2019-09-30'))
ax.set_ylim(0, 2625000)
ax2.set_ylim(0, 20)

# path to flights netcdf
file = './lidar_depths_wy2019.nc'

# open the file
ncf = nc.Dataset(file, 'r')

# get all of the water year hour numbers in the 'time' variable
times = ncf.variables['time'][:]

# close the file
ncf.close()

# get flight dates
def calculate_date_from_wyhr(wyhr, year):
    """
    Takes in the integer of water year hours and an integer year and
    returns the date
    """

    start = datetime(year=year-1, month=10, day=1)

    delta = timedelta(hours = wyhr)
    return start+delta

# convert each water year hour to a date and put them in a list
dates = []
for t in times:
    date = calculate_date_from_wyhr(int(t),2019)
    dates.append(date)

# loop through dates to plot lines
for i,date in enumerate(dates):
    if i == 0:
        lbl = 'Flight Dates'
    else:
        lbl = '__nolabel__'
    ax.axvline(x=date.date(), linestyle=':', linewidth=0.75, color='k', label=lbl)

fig1.legend(fontsize=6, loc="upper left", bbox_to_anchor=(0.75, 0.5))
plt.show()
plt.close()
