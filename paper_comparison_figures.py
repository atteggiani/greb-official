# LIBRARIES
from greb_climatevar import *
ignore_warnings()

def to_regional_mean(data,lats,lons):
    ind_st=to_greb_indexes(lats[0],lons[0])
    ind_end=to_greb_indexes(lats[1],lons[1])
    return data[...,ind_st[0]:ind_end[0],ind_st[1]:ind_end[1]].mean(axis=-1).mean(axis=-1)

def mean_20s(data):
    return data[20:30,...].mean(axis=0)

def mean_70s(data):
    return data[70:80,...].mean(axis=0)

def to_celsius(t):
    return t-273.15

def plot_tsurf(tsurf,labels=None):
    plt.figure()
    plt.plot(tsurf[0],color='black',linewidth=2,label='baseline')
    for t,l in zip(tsurf[1:],labels[1:]):
        plt.plot(t,label=l)
    plt.legend(loc='upper right',bbox_to_anchor=(-0.15,1))
    plt.title('Surface Temperature')
    plt.xlabel('years')
    plt.ylabel('tsurf (°C)')

def plot_precip(precip,labels=None):
    plt.figure()
    plt.plot(precip[0],color='black',linewidth=2,label='baseline')
    for t,l in zip(precip[1:],labels[1:]):
        plt.plot(t,label=l)
    plt.legend(loc='upper right',bbox_to_anchor=(-0.15,1))
    plt.title('Precipitation')
    plt.xlabel('years')
    plt.ylabel('precip (mm/d)')

def plot_std(tsurf,precip,areaspec,filespec):
    from matplotlib.lines import Line2D
    if not isinstance(areaspec,list): areaspec = [areaspec]
    colors=['g','b','r','orange','c','m','y','k']
    markers=['o','^','s']
    sz = 50
    plt.figure()
    for ind in np.arange(len(areaspec)):
        # 70s
        for ts,p,c in zip(tsurf[ind],precip[ind],colors):
            plt.scatter(ts,p,color=c, marker = markers[ind], s = sz)

    circle=plt.Circle((0, 0), 1, color='k', fill=False)
    plt.gca().add_artist(circle)

    legend_elements = [Line2D([0],[0], color=c, lw=3, label=fs) for fs,c in zip(filespec,colors)]+\
                      [Line2D([0],[0], color='w', marker = m, markeredgecolor = 'k', \
                       markerfacecolor='w', markersize=10, label=asp) for m,asp \
                       in zip(markers,areaspec)]

    for m,asp in zip(markers,areaspec): plt.scatter(0,0, marker = 'o', s = sz, \
                                        facecolor = None, edgecolor = 'black', \
                                                      visible=0,label = 'India')

    plt.xticks(np.arange(-8,8+1,1))
    plt.ylim([-2,2])
    plt.legend(handles=legend_elements,loc='upper right',
               bbox_to_anchor=(-0.1,1))
    plt.xlabel('Temperature',)
    plt.ylabel('Precipitation',rotation=0)
    plt.gca().spines['left'].set_position(('data', 0))
    plt.gca().spines['bottom'].set_position(('data', 0))
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().xaxis.set_label_coords(0.2, 0.4)
    plt.gca().yaxis.set_label_coords(0.5, 1.02)

dsk='/Users/dmar0022/Desktop/'
file_control = constants.control_def_file()
file_obs=['/Users/dmar0022/university/phd/data/NCEP-NCAR/air_temperature' + \
                '_2m_greb_grid/air.2m.gauss.{}_greb_grid.nc'.format(f) for f \
                in np.arange(1990,2000)]
files = []
files.append(constants.output_folder()+'/scenario.exp-20.2xCO2_80yrs.bin')
files.append(constants.output_folder()+'/scenario.exp-931.geoeng.sw.artificial.frominput-3.75_80yrs.bin')
files.append(constants.output_folder()+'/scenario.exp-931.geoeng.sw.artificial.frominput-7.4_80yrs.bin')
files.append(constants.output_folder()+'/scenario.exp-931.geoeng.sw.artificial.frominput-7.45_80yrs.bin')
files.append(constants.output_folder()+'/scenario.exp-931.geoeng.sw.artificial.frominput-7.5_80yrs.bin')
files.append(constants.output_folder()+'/scenario.exp-931.geoeng.sw.artificial.frominput-7.55_80yrs.bin')
files.append(constants.output_folder()+'/scenario.exp-931.geoeng.sw.artificial.frominput-7.6_80yrs.bin')
files.append(constants.output_folder()+'/scenario.exp-931.geoeng.sw.artificial.frominput-7.65_80yrs.bin')

filespec=['-3.75','-7.4','-7.45','-7.5','-7.55','-7.6','-7.65']
filespec=['baseline']+['{} W/m2'.format(fs) for fs in filespec]


india=[(8,33),(69,85)]
china=[(24,45),(80,120)]
aus=[(12,38),(114,153)]
areaspec=['india','china','australia']
# 'SOLAR'
# sw_obs = [iris.load_cube(f).data.squeeze() for f in file_obs]
# sw_obs = [np.delete(f,59,0) if f.shape[0] == 366 else f for f in sw_obs]
# sw_obs = np.vstack(sw_obs).reshape(10,365,48,96)

# 'TSURF'
ts_ctl = to_celsius(data_from_binary(file_control)['tsurf'])
ts = [to_celsius(data_from_binary(f)['tsurf']).reshape(80,12,48,96) for f in files]

ts_ctl_gm = ts_ctl.mean()
ts_gm = [np.insert(x.reshape(x.shape[0],-1).mean(axis=-1),0,ts_ctl_gm) for x in ts]

ts_anom_jja_70s = [mean_70s((x-ts_ctl)[:,5:8,...].mean(axis=1)) for x in ts]
ts_anom_djf_70s = [mean_70s((x-ts_ctl)[:,[0,1,-1],...].mean(axis=1)) for x in ts]

ts_base_std=(ts[0]-ts_ctl).std(axis=1)
ts_anom_jja_stdunit = [(x-ts_ctl)[:,5:8,...].mean(axis=1)/ts_base_std for x in ts[1:]]

ts_anom_jja_stdunit_20s = [mean_20s(x) for x in ts_anom_jja_stdunit]
ts_anom_jja_stdunit_70s = [mean_70s(x) for x in ts_anom_jja_stdunit]

# India
ts_anom_jja_stdunit_20s_india = [to_regional_mean(x,*india) for x in ts_anom_jja_stdunit_20s]
ts_anom_jja_stdunit_70s_india = [to_regional_mean(x,*india) for x in ts_anom_jja_stdunit_70s]

# China
ts_anom_jja_stdunit_20s_china = [to_regional_mean(x,*china) for x in ts_anom_jja_stdunit_20s]
ts_anom_jja_stdunit_70s_china = [to_regional_mean(x,*china) for x in ts_anom_jja_stdunit_70s]

# Australia
ts_anom_jja_stdunit_20s_aus = [to_regional_mean(x,*aus) for x in ts_anom_jja_stdunit_20s]
ts_anom_jja_stdunit_70s_aus = [to_regional_mean(x,*aus) for x in ts_anom_jja_stdunit_70s]

ts_anom_jja_stdunit_70s_all = [ts_anom_jja_stdunit_70s_india,ts_anom_jja_stdunit_70s_china,ts_anom_jja_stdunit_70s_aus]
# //==========================================================================//
# //==========================================================================//
# //==========================================================================//

# 'PRECIP'
p_ctl = data_from_binary(file_control)['precip']*-86400
p = [(data_from_binary(f)['precip']).reshape(80,12,48,96)*-86400 for f in files]

p_ctl_gm = p_ctl.mean()
p_gm = [np.insert(x.reshape(x.shape[0],-1).mean(axis=-1),0,p_ctl_gm) for x in p]

p_anom_jja_70s = [mean_70s((x-p_ctl)[:,5:8,...].mean(axis=1)) for x in p]
p_anom_djf_70s = [mean_70s((x-p_ctl)[:,[0,1,-1],...].mean(axis=1)) for x in p]

p_base_std=(p[0]-p_ctl).std(axis=1)
p_anom_jja_stdunit = [(x-p_ctl)[:,5:8,...].mean(axis=1)/p_base_std for x in p[1:]]

p_anom_jja_stdunit_20s = [mean_20s(x) for x in p_anom_jja_stdunit]
p_anom_jja_stdunit_70s = [mean_70s(x) for x in p_anom_jja_stdunit]

# India
p_anom_jja_stdunit_20s_india = [to_regional_mean(x,*india) for x in p_anom_jja_stdunit_20s]
p_anom_jja_stdunit_70s_india = [to_regional_mean(x,*india) for x in p_anom_jja_stdunit_70s]

# China
p_anom_jja_stdunit_20s_china = [to_regional_mean(x,*china) for x in p_anom_jja_stdunit_20s]
p_anom_jja_stdunit_70s_china = [to_regional_mean(x,*china) for x in p_anom_jja_stdunit_70s]

# Australia
p_anom_jja_stdunit_20s_aus = [to_regional_mean(x,*aus) for x in p_anom_jja_stdunit_20s]
p_anom_jja_stdunit_70s_aus = [to_regional_mean(x,*aus) for x in p_anom_jja_stdunit_70s]

p_anom_jja_stdunit_70s_all = [p_anom_jja_stdunit_70s_india,p_anom_jja_stdunit_70s_china,p_anom_jja_stdunit_70s_aus]
# //==========================================================================//
# //==========================================================================//
# //==========================================================================//

#PLOT
plot_tsurf(ts_gm,filespec)
plt.savefig(dsk+'tsurf.png', bbox_inches='tight',dpi=300)

plot_precip(p_gm,filespec)
plt.savefig(dsk+'precip.png', bbox_inches='tight',dpi=300)

plot_std(ts_anom_jja_stdunit_70s_all,p_anom_jja_stdunit_70s_all,
         areaspec,filespec[1:])
plt.savefig(dsk+'std.png', bbox_inches='tight',dpi=300)

plot_std(ts_anom_jja_stdunit_70s_all,p_anom_jja_stdunit_70s_all,
         areaspec,filespec[1:])
plt.xlim(-1.2,1.2)
plt.ylim(-1,1)
plt.savefig(dsk+'std_zoom.png', bbox_inches='tight',dpi=300)
