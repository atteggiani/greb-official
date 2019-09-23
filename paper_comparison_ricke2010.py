from myfuncs import *
from greb_climatevar import *

def plot_tsurf(tsurf,labels):
    from matplotlib.ticker import AutoMinorLocator
    cmap=plt.get_cmap('Spectral_r')
    colors = [cmap(i) for i in np.linspace(0, 1, len(tsurf[1:]))]
    plt.figure()
    plt.plot(tsurf[0],color='black',linewidth=2,label=labels[0])
    for t,l,c in zip(tsurf[1:],labels[1:],colors):
        plt.plot(t,label=l,color=c)
    plt.legend(loc='upper right',bbox_to_anchor=(-0.15,1.05),fontsize = 'xx-small')
    plt.title('Surface Temperature')
    plt.xlabel('years')
    plt.ylabel('tsurf (°C)')
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator())
    plt.grid(which='both',linestyle='--')

def plot_precip(precip,labels):
    from matplotlib.ticker import AutoMinorLocator
    cmap=plt.get_cmap('Spectral_r')
    colors = [cmap(i) for i in np.linspace(0, 1, len(precip[1:]))]
    plt.figure()
    plt.plot(precip[0],color='black',linewidth=2,label=labels[0])
    for t,l,c in zip(precip[1:],labels[1:],colors):
        plt.plot(t,label=l,color=c)
    plt.legend(loc='upper right',bbox_to_anchor=(-0.15,1.05),fontsize = 'xx-small')
    plt.title('Precipitation')
    plt.xlabel('years')
    plt.ylabel('precip (mm/d)')
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator())
    plt.grid(which='both',linestyle='--')

def scatter_plot(data,areaspec,filespec):
    from matplotlib.ticker import AutoMinorLocator,MultipleLocator
    from matplotlib.lines import Line2D

    if not isinstance(areaspec,dict):
        raise TypeError('areaspec must be a dictionary in the form:\n'+
                        "{'area_name1': [[lat_start,lat_end],[lon_start,lon_end]], 'area_name2': ... }")
    data_new = [[d.sel(lat=slice(*v[0]),lon=slice(*v[1])).global_mean() for d in data] for v in areaspec.values()]
    cmap=plt.get_cmap('Spectral_r')
    colors = [cmap(i) for i in np.linspace(0, 1, len(data))]
    markers=['o','^','s','X','v','*',"<","P","D"]
    sz = 20
    plt.figure()
    for d_n,m in zip(data_new,markers):
        for d,c in zip(d_n,colors):
            plt.scatter(d.tsurf,d.precip,facecolor="None",edgecolor=c, marker = m, s = sz)

    legend_elements = [Line2D([0],[0], color=c, lw=3, label=fs) for fs,c in zip(filespec,colors)]+\
                      [Line2D([0],[0], color='w', lw=5)]+\
                      [Line2D([0],[0], color='w', marker = m, markeredgecolor = 'k', \
                       markerfacecolor='w', markersize=5, label=asp) for m,asp \
                       in zip(markers,areaspec.keys())]

    plt.xticks(np.arange(-1.5,1.5+0.5,0.5))
    plt.yticks(np.arange(-0.5,0.5+0.25,0.25))
    plt.legend(handles=legend_elements,loc='upper right',
               bbox_to_anchor=(-0.1,1.1),fontsize = 'xx-small')
    plt.xlabel('Temperature [°C]',)
    plt.ylabel('Precipitation [mm/d]',rotation=0)
    plt.gca().spines['left'].set_position(('data', 0))
    plt.gca().spines['bottom'].set_position(('data', 0))
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().xaxis.set_label_coords(0.12, 0.68)
    plt.gca().yaxis.set_minor_locator(MultipleLocator(base=0.05))
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator())
    plt.gca().yaxis.set_label_coords(0.5, 1.03)

outpath='/Users/dmar0022/Desktop/new/'
filespec=np.arange(0.977,0.982+0.0002,0.0002)
files = [constants.output_folder()+'/scenario.exp-931.geoeng.sw.artificial.frominput_x{:g}_80yrs'.format(f) for f in filespec]
files.insert(0,constants.output_folder()+'/scenario.exp-20.2xCO2_80yrs.bin')
namespec=['NO-SRM']+['{:5.4f}'.format(f) for f in filespec]
areaspec={'india':[(8,33),(69,85)],
          'china':[(24,45),(80,120)],
          'australia':[(-38,-12),(114,153)],
          'central_africa':[(-17,15),(6,35)],
          'papua_new_guinea':[(-9,1),(130,155)],
          'russia':[(55,70),(50,150)]}

# 'TSURF'
ts_ctl = from_binary(constants.control_def_file(),time_group='month').tsurf.to_celsius(copy=False)
ts_ctl_gm = ts_ctl.global_mean().annual_mean().assign_coords(time=0)

ts = [from_binary(f,time_group='month').tsurf.to_celsius(copy=False) for f in files]
ts_gm = [DataArray(xr.concat([ts_ctl_gm,t.global_mean()],dim='time')) for t in ts]

ts_high_srm=sum(ts[1:6])/5
ts_low_srm=sum(ts[-6:-1])/5

ind_best = np.argmin([np.abs((t-ts_ctl_gm).mean()) for t in ts_gm])
alpha_best = round(filespec[ind_best],4)
ts_best_srm = ts[ind_best]

ts_anom_jja_70s = [from_binary(f).tsurf.anomalies().isel(time=slice(70*12,80*12)).groupby('time.season').mean('time',keep_attrs=True).sel(season='JJA') for f in files[1:]]

# //==========================================================================//

# 'PRECIP'
p_ctl = from_binary(constants.control_def_file(),time_group='month').precip
p_ctl_gm = p_ctl.global_mean().annual_mean().assign_coords(time=0)

p = [from_binary(f,time_group='month').precip for f in files]
p_gm = [DataArray(xr.concat([p_ctl_gm,t.global_mean()],dim='time')) for t in p]

p_high_srm=sum(p[1:6])/5
p_low_srm=sum(p[-6:-1])/5

p_best_srm = p[ind_best]

p_anom_jja_70s = [from_binary(f).precip.anomalies().isel(time=slice(70*12,80*12)).groupby('time.season').mean('time',keep_attrs=True).sel(season='JJA') for f in files[1:]]

# //==========================================================================//

data = [from_binary(f).to_celsius()[['precip','tsurf']] for f in files]

# Annual global mean
ctl_gm = from_binary(constants.control_def_file()).global_mean().annual_mean().assign_coords(time=0).to_celsius()[['precip','tsurf']]
_gm = [from_binary(f,'year').to_celsius()[['precip','tsurf']].global_mean() for f in files]
gm = [Dataset(xr.concat([d,ctl_gm],dim='time',positions=[list(np.arange(1,d.dims['time']+1))+[0]]),attrs=d.attrs) for d in _gm]
for d in gm:
    for var in d:
        d._variables[var].attrs['grouped_by'] = 'year'

high_srm=(sum(data[1:6])/5).annual_mean()
low_srm=(sum(data[-6:-1])/5).annual_mean()

ind_best=np.argmin(np.abs([d.global_mean().annual_mean().anomalies().tsurf.values for d in data]))
alpha_best = round(filespec[ind_best],4)
best_srm = data[ind_best].annual_mean()

anom_jja_70s = [Dataset(d.anomalies().isel(time=slice(70*12,80*12)).groupby('time.season').mean('time',keep_attrs=True).sel(season='JJA'),attrs=d.attrs) for d in data[1:]]

#PLOT TSURF
plot_tsurf([g.tsurf for g in gm],namespec)
plt.savefig(outpath+'tsurf.png', bbox_inches='tight',dpi=400)
#PLOT PRECIP
plot_precip([g.precip for g in gm],namespec)
plt.savefig(outpath+'precip.png', bbox_inches='tight',dpi=400)
#SCATTER PLOT TSURF/PRECIP
scatter_plot(anom_jja_70s,areaspec,namespec[1:])
plt.savefig(outpath+'std.png', bbox_inches='tight',dpi=300)

#PLOT MAPS LOW SRM
low_srm.tsurf.anomalies().plotvar(name='low_srm',outpath=outpath)
low_srm.precip.anomalies().plotvar(name='low_srm',outpath=outpath)

#PLOT MAPS HIGH SRM
high_srm.tsurf.anomalies().plotvar(name='high_srm',outpath=outpath)
high_srm.precip.anomalies().plotvar(name='high_srm',outpath=outpath)

#PLOT MAPS BEST SRM
best_srm.tsurf.anomalies().plotvar(name='best_srm',outpath=outpath)
best_srm.precip.anomalies().plotvar(name='best_srm',outpath=outpath)
