from myfuncs import *

def to_regional_mean(data,lats,lons):
    ind_st=to_greb_indexes(lats[0],lons[0])
    ind_end=to_greb_indexes(lats[1],lons[1])
    return data[...,ind_st[0]:ind_end[0],ind_st[1]:ind_end[1]].mean(axis=-1).mean(axis=-1)

def mean_20s(data):
    return data[20:30,...].mean(axis=0)

def mean_70s(data):
    return data[70:80,...].mean(axis=0)

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

def scatter_plot(tsurf,precip,areaspec,filespec):
    from matplotlib.ticker import AutoMinorLocator,MultipleLocator
    from matplotlib.lines import Line2D
    if not isinstance(areaspec,list): areaspec = [areaspec]
    cmap=plt.get_cmap('Spectral_r')
    colors = [cmap(i) for i in np.linspace(0, 1, len(tsurf[0][1:]))]
    markers=['o','^','s','X','v','*']
    sz = 20
    plt.figure()
    for area in np.arange(len(areaspec)):
        # 70s
        for ts,p,c in zip(tsurf[area],precip[area],colors):
            plt.scatter(ts,p,facecolor="None",edgecolor=c, marker = markers[area], s = sz)

    # circle=plt.Circle((0, 0), 1, color='k', fill=False)
    # plt.gca().add_artist(circle)

    legend_elements = [Line2D([0],[0], color=c, lw=3, label=fs) for fs,c in zip(filespec,colors)]+\
                      [Line2D([0],[0], color='w', marker = m, markeredgecolor = 'k', \
                       markerfacecolor='w', markersize=5, label=asp) for m,asp \
                       in zip(markers,areaspec)]

    # for m,asp in zip(markers,areaspec): plt.scatter(0,0, marker = 'o', s = sz, \
    #                                     facecolor = None, edgecolor = 'black', \
    #                                                   visible=0,label = 'India')

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
    plt.gca().xaxis.set_label_coords(0.15, 0.57)
    plt.gca().yaxis.set_minor_locator(MultipleLocator(base=0.05))
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator())
    plt.gca().yaxis.set_label_coords(0.4, 1.03)

outpath='/Users/dmar0022/Desktop/'
filespec=np.arange(0.977,0.982+0.0002,0.0002)
files = [constants.output_folder()+'/scenario.exp-931.geoeng.sw.artificial.frominput_x{:g}_80yrs'.format(f) for f in filespec]
files.insert(0,constants.output_folder()+'/scenario.exp-20.2xCO2_80yrs.bin')
namespec=['NO-SRM']+['{:g}'.format(f) for f in filespec]
areaspec={'india':[(8,33),(69,85)],'china':[(24,45),(80,120)],
              'australia':[(-38,-12),(114,153)],'central_africa':[(-17,15),(6,35)],
              'papua_new_guinea':[(-9,1),(130,155)],'russia':[(55,70),(50,150)]}

# 'TSURF'
ts_ctl = from_binary(constants.control_def_file(),time_group='month').tsurf.to_celsius(copy=False)
ts_ctl_gm = ts_ctl.global_mean().mean('time').assign_coords(time=0)

ts = [from_binary(f,time_group='month').tsurf.to_celsius(copy=False) for f in files]
ts_gm = [DataArray(xr.concat([ts_ctl_gm,t.global_mean()],dim='time')) for t in ts]

ts_high_srm=sum(ts[1:6])/5
ts_low_srm=sum(ts[-6:-1])/5
ind_best = np.argmin(np.abs([np.mean(t) for t in (ts_gm[1:]-ts_ctl_gm)]))
alpha_best = round(filespec[ind_best],4)
ts_best_srm = ts[ind]


_ts_ctl = ts_ctl.data.data
_ts = [d.data.data.reshape(-1,12,48,96) for d in ts[1:]]

ts_anom_jja = [(x-_ts_ctl)[:,5:8,...].mean(axis=1) for x in _ts]

ts_anom_jja_70s = [mean_70s(x) for x in ts_anom_jja]

# Regional means
ts_anom_jja_70s_all =[]
for reg in areaspec:
    ts_anom_jja_70s_all.append([to_regional_mean(x,*eval(reg)) for x in ts_anom_jja_70s])

# //==========================================================================//
# //==========================================================================//
# //==========================================================================//

# 'PRECIP'
p_ctl = cube_from_binary(file_control)
p_ctl = p_ctl[[v.var_name for v in p_ctl].index('precip')]
p_ctl_gm = global_mean(p_ctl).data.data.mean()

ind = [v.var_name for v in cube_from_binary(files[0])].index('precip')
p = [cube_from_binary(f)[ind] for f in files]
p_gm = [np.insert(global_mean(d).data.data.reshape(80,12).mean(axis=-1),0,p_ctl_gm) for d in p]

p_high_srm=sum(p[1:6])/5
p_low_srm=sum(p[-6:-1])/5
p_best_srm = p[ind_best]

_p_ctl = p_ctl.data.data
_p = [d.data.data.reshape(-1,12,48,96) for d in p[1:]]

p_anom_jja = [(x-_p_ctl)[:,5:8,...].mean(axis=1) for x in _p]

p_anom_jja_70s = [mean_70s(x) for x in p_anom_jja]

# Regional means
p_anom_jja_70s_all =[]
for reg in areaspec:
    p_anom_jja_70s_all.append([to_regional_mean(x,*eval(reg)) for x in p_anom_jja_70s])

# //==========================================================================//
# //==========================================================================//
# //==========================================================================//

#PLOT TSURF
plot_tsurf(ts_gm,namespec)
plt.savefig(outpath+'tsurf.png', bbox_inches='tight',dpi=400)
#PLOT PRECIP
plot_precip(p_gm,namespec)
plt.savefig(outpath+'precip.png', bbox_inches='tight',dpi=400)
#SCATTER PLOT TSURF/PRECIP
scatter_plot(ts_anom_jja_70s_all,p_anom_jja_70s_all,
         areaspec,namespec[1:])
plt.savefig(outpath+'std.png', bbox_inches='tight',dpi=300)

#PLOT MAPS LOW SRM
lt=plot_param.from_cube(ts_low_srm,units='°C',cmaplev=np.arange(-2,2+0.1,0.1),
                       cbticks=np.arange(-2,2+0.5,0.5), tit='Low SRM tsurf anomalies',
                       varname='ts_low_srm')
ts_ctl.var_name = ts_low_srm.var_name
plt.figure()
lt.to_annual_mean().to_anomalies(ts_ctl).plot(outpath=outpath)

lp=plot_param.from_cube(p_low_srm,units='mm/d',cmaplev=np.arange(-1,1+0.1,0.1),
                       cbticks=np.arange(-1,1+0.2,0.2), tit='Low SRM precip anomalies',
                       varname='p_low_srm')
p_ctl.var_name = p_low_srm.var_name
plt.figure()
lp.to_annual_mean().to_anomalies(p_ctl).plot(outpath=outpath)

#PLOT MAPS HIGH SRM
ht=plot_param.from_cube(ts_high_srm,units='°C',cmaplev=np.arange(-2,2+0.1,0.1),
                       cbticks=np.arange(-2,2+0.5,0.5), tit='High SRM tsurf anomalies',
                       varname='ts_high_srm')
ts_ctl.var_name = ts_high_srm.var_name
plt.figure()
ht.to_annual_mean().to_anomalies(ts_ctl).plot(outpath=outpath)

hp=plot_param.from_cube(p_high_srm,units='mm/d',cmaplev=np.arange(-1,1+0.1,0.1),
                       cbticks=np.arange(-1,1+0.2,0.2), tit='High SRM precip anomalies',
                       varname='p_high_srm')
p_ctl.var_name = p_high_srm.var_name
plt.figure()
hp.to_annual_mean().to_anomalies(p_ctl).plot(outpath=outpath)

#PLOT MAPS BEST SRM
bt=plot_param.from_cube(ts_best_srm,units='°C',cmaplev=np.arange(-2,2+0.1,0.1),
                       cbticks=np.arange(-2,2+0.5,0.5),
                       tit='Best SRM tsurf anomalies - alpha = {:g}'.format(alpha_best),
                       varname='ts_best_srm')
ts_ctl.var_name = ts_best_srm.var_name
plt.figure()
bt.to_annual_mean().to_anomalies(ts_ctl).plot(outpath=outpath)

bp=plot_param.from_cube(p_best_srm,units='mm/d',cmaplev=np.arange(-1,1+0.1,0.1),
                       cbticks=np.arange(-1,1+0.2,0.2),
                       tit='Best SRM precip anomalies - alpha = {:g}'.format(alpha_best),
                       varname='p_best_srm')
p_ctl.var_name = p_best_srm.var_name
plt.figure()
bp.to_annual_mean().to_anomalies(p_ctl).plot(outpath=outpath)
