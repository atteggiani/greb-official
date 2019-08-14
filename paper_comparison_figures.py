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

def plot_std(tsurf,precip,areaspec,filespec):
    from matplotlib.lines import Line2D
    if not isinstance(areaspec,list): areaspec = [areaspec]
    cmap=plt.get_cmap('Spectral_r')
    colors = [cmap(i) for i in np.linspace(0, 1, len(tsurf[0][1:]))]
    markers=['o','^','s']
    sz = 20
    plt.figure()
    for area in np.arange(len(areaspec)):
        # 70s
        for ts,p,c in zip(tsurf[area],precip[area],colors):
            plt.scatter(ts,p,color=c, marker = markers[area], s = sz)

    circle=plt.Circle((0, 0), 1, color='k', fill=False)
    plt.gca().add_artist(circle)

    legend_elements = [Line2D([0],[0], color=c, lw=3, label=fs) for fs,c in zip(filespec,colors)]+\
                      [Line2D([0],[0], color='w', marker = m, markeredgecolor = 'k', \
                       markerfacecolor='w', markersize=5, label=asp) for m,asp \
                       in zip(markers,areaspec)]

    for m,asp in zip(markers,areaspec): plt.scatter(0,0, marker = 'o', s = sz, \
                                        facecolor = None, edgecolor = 'black', \
                                                      visible=0,label = 'India')

    plt.xticks(np.arange(-8,8+1,1))
    plt.ylim([-2,2])
    plt.legend(handles=legend_elements,loc='upper right',
               bbox_to_anchor=(-0.1,1.1),fontsize = 'xx-small')
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

# load files from HadCM3 model
file_hadCM3_control_ts = r'/Users/dmar0022/university/phd/data/HadCM3/HADCM3_20C3M_1_G_tas_1990_1999.nc'
file_hadCM3_noSRM_ts = r'/Users/dmar0022/university/phd/data/HadCM3/HADCM3_SRA1B_1_G_tas_2000_2080.nc'
file_hadCM3_control_pr = r'/Users/dmar0022/university/phd/data/HadCM3/HADCM3_20C3M_1_G_pr_1990_1999.nc'
file_hadCM3_noSRM_pr = r'/Users/dmar0022/university/phd/data/HadCM3/HADCM3_SRA1B_1_G_pr_2000_2080.nc'
files_hadCM3_ts=[file_hadCM3_control_ts,file_hadCM3_noSRM_ts]
files_hadCM3_pr=[file_hadCM3_control_pr,file_hadCM3_noSRM_pr]

filespec=np.arange(0.974,0.98,0.0002)
files = [constants.output_folder()+'/scenario.exp-931.geoeng.sw.artificial.frominput_x{:g}_80yrs'.format(f) for f in filespec]
files.insert(0,constants.output_folder()+'/scenario.exp-20.2xCO2_80yrs.bin')
namespec=['NO-SRM']+['{:g}'.format(f) for f in filespec[1:]]

india=[(8,33),(69,85)]
china=[(24,45),(80,120)]
aus=[(12,38),(114,153)]
areaspec=['india','china','australia']

# 'TSURF'
ts_ctl = cube_from_binary(file_control)
ts_ctl = to_celsius(ts_ctl[[v.var_name for v in ts_ctl].index('tsurf')])
ts_hadCM3 = [to_celsius(iris.load_cube(f)) for f in files_hadCM3_ts]
ts_hadCM3 = [constants.to_greb_grid(t,ts_ctl,'linear') for t in ts_hadCM3]

ts_ctl = ts_ctl.data.data
ts = [to_celsius(data_from_binary(f)['tsurf']).reshape(80,12,48,96) for f in files]
ts_hadCM3 = [t.data.data for t in ts_hadCM3]
ts_hadCM3[0] = ts_hadCM3[0].mean(axis=0)
ts_hadCM3[1] = ts_hadCM3[1].reshape(81,12,48,96)[1:,...]

ts_hadCM3[1].reshape(80,-1).mean(axis=-1)
ts_hadCM3[1].reshape(81,-1).mean(axis=-1)

ts_ctl_gm = ts_ctl.mean()
ts_gm = [np.insert(x.reshape(x.shape[0],-1).mean(axis=-1),0,ts_ctl_gm) for x in ts]

ts_base_std = (ts_hadCM3[1]-ts_hadCM3[0]).std(axis=1)
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
p_ctl = cube_from_binary(file_control)
p_ctl = p_ctl[[v.var_name for v in p_ctl].index('precip')]
p_hadCM3 = [iris.load_cube(f)*-86400 for f in files_hadCM3_pr]
p_hadCM3 = [constants.to_greb_grid(t,p_ctl) for t in p_hadCM3]

p_ctl = p_ctl.data.data
p = [(data_from_binary(f)['precip']).reshape(80,12,48,96)*-86400 for f in files]
p_hadCM3 = [p.data.data for p in p_hadCM3]
p_hadCM3[0] = p_hadCM3[0].mean(axis=0)
p_hadCM3[1] = p_hadCM3[1].reshape(81,12,48,96)[1:,...]

p_ctl_gm = p_ctl.mean()
p_gm = [np.insert(x.reshape(x.shape[0],-1).mean(axis=-1),0,p_ctl_gm) for x in p]

p_base_std=(p_hadCM3[1]-p_hadCM3[0]).std(axis=1)
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
plot_tsurf(ts_gm,namespec)
plt.savefig(dsk+'tsurf1.png', bbox_inches='tight',dpi=400)

plot_precip(p_gm,namespec)
plt.savefig(dsk+'precip.png', bbox_inches='tight',dpi=400)

plot_std(ts_anom_jja_stdunit_70s_all,p_anom_jja_stdunit_70s_all,
         areaspec,namespec[1:])
plt.savefig(dsk+'std.png', bbox_inches='tight',dpi=300)

plot_std(ts_anom_jja_stdunit_70s_all,p_anom_jja_stdunit_70s_all,
         areaspec,namespec[1:])
plt.xlim(-1.2,1.2)
plt.ylim(-1,1)
plt.savefig(dsk+'std_zoom.png', bbox_inches='tight',dpi=300)
