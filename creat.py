from datetime import datetime

import numpy as np
import pandas as pd

import netCDF4 as nc


## create NetCDF file
newfile = nc.Dataset('newfile.nc', 'w', format='NETCDF4')

## define dimesions
long = newfile.createDimension('longitude', size=360)
lati = newfile.createDimension('latitude', size=180)
heights = newfile.createDimension('height', size=15)
times = newfile.createDimension('time', size=None)

## define variables for storing data
lon = newfile.createVariable('lon', 'f4', dimensions='longitude')
lat = newfile.createVariable('lat', 'f4', dimensions='latitude')
height = newfile.createVariable('height', 'f4', dimensions='height')
time = newfile.createVariable('times', 'S19', dimensions='time')
temps = newfile.createVariable('temperature', 'f4', dimensions=('longitude', 'latitude', 'height', 'time'))

## generate random values
temp = np.random.randint(-40, 40, size=(360, 180, 15, 24))

date_range = pd.date_range(datetime(2019, 6, 1, 0), datetime(2019, 6, 1, 23), freq='1h')

## add data to variables
lon[:] = np.arange(-180, 180)
lat[:] = np.arange(-90, 90)
height[:] = [10, 50, 100, 150, 200, 500, 1000, 1500, 2000, 3000, 4000, 5000, 6000, 8000, 10000]
temps[...] = temp
for i in range(24):
    time[i] = date_range[i].strftime('%Y-%m-%d %H:%M:%S')

## add attributes    
#add global attributes
newfile.title = 'Example of create NetCDF file using netcdf4-python'
newfile.start_time = time[i]
newfile.times = time.shape[0]
newfile.history = 'Created ' + datetime(2019, 6, 1, 0, 0, 0).strftime('%Y-%m-%d %H:%M%S')

#add local attributes to variable
lon.description = 'longitude, west is negative'
lon.units = 'degrees east'

lat.description = 'latitude, south is negative'
lat.units = 'degrees north'

time.description = 'time, unlimited dimension'
time.units = 'times since {0:s}'.format(time[0])

temps.description = 'temperature, random value generated by numpy'
temps.units = 'degree'

height.description = 'height, above ground level'
height.units = 'meters'    

## close file
newfile.close()