# LIBRARIES
from greb_climatevar import * # Import self defined classes and function
ignore_warnings()
import bottleneck as bn

def to_celsius(t):
    return t-273.15

file_hadCM3_control_ts = r'/Users/dmar0022/university/phd/data/HadCM3/HADCM3_20C3M_1_G_tas_1990_1999.nc'
file_hadCM3_noSRM_ts = r'/Users/dmar0022/university/phd/data/HadCM3/HADCM3_SRA1B_1_G_tas_2000_2080.nc'
file_hadCM3_control_pr = r'/Users/dmar0022/university/phd/data/HadCM3/HADCM3_20C3M_1_G_pr_1990_1999.nc'
file_hadCM3_noSRM_pr = r'/Users/dmar0022/university/phd/data/HadCM3/HADCM3_SRA1B_1_G_pr_2000_2080.nc'
files_hadCM3_ts=[file_hadCM3_control_ts,file_hadCM3_noSRM_ts]
files_hadCM3_pr=[file_hadCM3_control_pr,file_hadCM3_noSRM_pr]

data_ts=[to_celsius(iris.load_cube(f).data) for f in files_hadCM3_ts]
data_pr=[to_celsius(iris.load_cube(f).data) for f in files_hadCM3_pr]
data_ts[0]
data_ts[1]

data=data_ts[1].reshape(81,12, 73, 96)
gm=data.reshape(81,-1).mean(axis=-1)
gm1=gm=data_ts[0].reshape(10,-1).mean(axis=-1)
plt.plot(gm)
plt.plot(gm1)
qplt.contourf(tas.collapsed('time',iris.analysis.MEAN))
