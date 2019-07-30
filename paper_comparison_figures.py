# LIBRARIES
from greb_climatevar import *
ignore_warnings()

def custom_cmap(cmap1,cmap2):
    import matplotlib.colors as mcolors
    colors1 = cmap2(np.linspace(0.15, 1, 129))
    colorwhite = [[1,1,1,1]]*66
    colors2 = cmap1(np.linspace(0, 0.85, 129))
    # combine them and build a new colormap
    colors = np.vstack((colors2, colorwhite, colors1))
    mycmap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
    return mycmap

def std_ratio(min=-1,max=1):
    a=np.logical_and(p_best_anom_jja_stdunit_70s >= min,p_best_anom_jja_stdunit_70s <= max)
    b=np.logical_and(ts_best_anom_jja_stdunit_70s >= min,ts_best_anom_jja_stdunit_70s <= max)
    return np.logical_and(a,b).sum()/(48*96)

def to_regional_mean(data,lats,lons):
    ind_st=to_greb_indexes(lats[0],lons[0])
    ind_end=to_greb_indexes(lats[1],lons[1])
    return data[...,ind_st[0]:ind_end[0],ind_st[1]:ind_end[1]].mean(axis=-1).mean(axis=-1)

def mean_20s(data):
    return data[20:30,...].mean(axis=0)

def mean_70s(data):
    return data[70:80,...].mean(axis=0)

def to_celsus(t):
    return t-273.15

def plot_tsurf():
    plt.figure()
    plt.plot(ts_base_gm,color='black',linewidth=2,label='baseline')
    plt.plot(ts_x1_1_gm,color='green',label='default x 1.1')
    plt.plot(ts_iter4_gm,color='blue',label='4th iter')
    plt.plot(ts_best_gm,color='red',label='best (18th iter)')
    plt.legend()
    plt.title('Surface Temperature')
    plt.xlabel('years')
    plt.ylabel('tsurf (°C)')

def plot_precip():
    plt.figure()
    plt.plot(p_base_gm,color='black',linewidth=2,label='baseline')
    plt.plot(p_x1_1_gm,color='green',label='default x 1.1')
    plt.plot(p_iter4_gm,color='blue',label='4th iter')
    plt.plot(p_best_gm,color='red',label='best (18th iter)')
    plt.legend()
    plt.title('Precipitation')
    plt.xlabel('years')
    plt.ylabel('precip (mm/d)')

def plot_cloud():
    x=constants.t().tolist()
    x=[from_greb_time(a) for a in x]
    plt.figure()
    plt.plot(x,cld_base_gm,color='black',linewidth=2,label='baseline')
    plt.plot(x,cld_x1_1_gm,color='green',label='default x 1.1')
    plt.plot(x,cld_iter4_gm,color='blue',label='4th iter')
    plt.plot(x,cld_best_gm,color='red',label='best (18th iter)')
    plt.legend()
    plt.grid()
    plt.title('Clouds')
    plt.ylim([0,1])
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.xlabel('months')
    plt.ylabel('clouds')

def plot_std():
    from matplotlib.lines import Line2D

    sz = 50
    plt.figure()
    # INDIA
    # 70s
    plt.scatter(ts_x1_1_anom_jja_stdunit_20s_india,p_x1_1_anom_jja_stdunit_20s_india,
                                           color='green', marker = 'o', s = sz)
    plt.scatter(ts_iter4_anom_jja_stdunit_20s_india,p_iter4_anom_jja_stdunit_20s_india,
                                            color='blue', marker = 'o', s = sz)
    plt.scatter(ts_best_anom_jja_stdunit_20s_india,p_best_anom_jja_stdunit_20s_india,
                                             color='red', marker = 'o', s = sz)
    # 20s
    plt.scatter(ts_x1_1_anom_jja_stdunit_70s_india,p_x1_1_anom_jja_stdunit_70s_india,
                                alpha=0.5, color='green', marker = 'o', s = sz)
    plt.scatter(ts_iter4_anom_jja_stdunit_70s_india,p_iter4_anom_jja_stdunit_70s_india,
                                 alpha=0.5, color='blue', marker = 'o', s = sz)
    plt.scatter(ts_best_anom_jja_stdunit_70s_india,p_best_anom_jja_stdunit_70s_india,
                                  alpha=0.5, color='red', marker = 'o', s = sz)
    # CHINA
    # 70s
    plt.scatter(ts_x1_1_anom_jja_stdunit_20s_china,p_x1_1_anom_jja_stdunit_20s_china,
                                           color='green', marker = '^', s = sz)
    plt.scatter(ts_iter4_anom_jja_stdunit_20s_china,p_iter4_anom_jja_stdunit_20s_china,
                                            color='blue', marker = '^', s = sz)
    plt.scatter(ts_best_anom_jja_stdunit_20s_china,p_best_anom_jja_stdunit_20s_china,
                                             color='red', marker = '^', s = sz)
    # 20s
    plt.scatter(ts_x1_1_anom_jja_stdunit_70s_china,p_x1_1_anom_jja_stdunit_70s_china,
                                alpha=0.5, color='green', marker = '^', s = sz)
    plt.scatter(ts_iter4_anom_jja_stdunit_70s_china,p_iter4_anom_jja_stdunit_70s_china,
                                 alpha=0.5, color='blue', marker = '^', s = sz)
    plt.scatter(ts_best_anom_jja_stdunit_70s_china,p_best_anom_jja_stdunit_70s_china,
                                  alpha=0.5, color='red', marker = '^', s = sz)
    # AUSTRALIA
    # 70s
    plt.scatter(ts_x1_1_anom_jja_stdunit_20s_aus,p_x1_1_anom_jja_stdunit_20s_aus,
                                           color='green', marker = 's', s = sz)
    plt.scatter(ts_iter4_anom_jja_stdunit_20s_aus,p_iter4_anom_jja_stdunit_20s_aus,
                                            color='blue', marker = 's', s = sz)
    plt.scatter(ts_best_anom_jja_stdunit_20s_aus,p_best_anom_jja_stdunit_20s_aus,
                                             color='red', marker = 's', s = sz)
    # 20s
    plt.scatter(ts_x1_1_anom_jja_stdunit_70s_aus,p_x1_1_anom_jja_stdunit_70s_aus,
                                alpha=0.5, color='green', marker = 's', s = sz)
    plt.scatter(ts_iter4_anom_jja_stdunit_70s_aus,p_iter4_anom_jja_stdunit_70s_aus,
                                 alpha=0.5, color='blue', marker = 's', s = sz)
    plt.scatter(ts_best_anom_jja_stdunit_70s_aus,p_best_anom_jja_stdunit_70s_aus,
                                  alpha=0.5, color='red', marker = 's', s = sz)

    circle=plt.Circle((0, 0), 1, color='k', fill=False)
    plt.gca().add_artist(circle)

    legend_elements = [Line2D([0],[0], color='green', lw=3, label='default x 1.1'),
                       Line2D([0],[0], color='blue', lw=3, label='4th iter'),
                       Line2D([0],[0], color='red', lw=3, label='best'),
                       Line2D([0],[0], color='w', marker = 'o', markeredgecolor = 'k',
                             markerfacecolor='w', markersize=10, label='India'),
                       Line2D([0],[0], color='w', marker = '^', markeredgecolor = 'k',
                       markerfacecolor='w', markersize=10, label='China'),
                       Line2D([0],[0], color='w', marker = 's', markeredgecolor = 'k',
                       markerfacecolor='w', markersize=10, label='China')]

    plt.scatter(0,0, marker = 'o', s = sz, facecolor = None, edgecolor = 'black',
                                                      visible=0,label = 'India')
    plt.scatter(0,0, marker = '^', s = sz, facecolor = None, edgecolor = 'black',
                                                      visible=0,label = 'China')
    plt.scatter(0,0, marker = 's', s = sz, facecolor = None, edgecolor = 'black',
                                                  visible=0,label = 'Australia')
    plt.legend(handles=legend_elements,loc=2)


    plt.xticks(np.arange(-5,2+1,1))
    plt.ylim([-1.2,1.2])
    plt.xlabel('Temperature',)
    plt.ylabel('Precipitation',rotation=0)
    plt.gca().spines['left'].set_position(('data', 0))
    plt.gca().spines['bottom'].set_position(('data', 0))
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().xaxis.set_label_coords(0.2, 0.4)
    plt.gca().yaxis.set_label_coords(0.73, 1.02)

dsk='/Users/dmar0022/Desktop/'
file_control = constants.control_def_file()
file_baseline = constants.output_folder()+'/scenario.exp-20.2xCO2_80yrs.bin'
file_best = constants.output_folder()+'/scenario.exp-930.geoeng.cld.artificial_best_80yrs.bin'
file_4th_iter = constants.output_folder()+'/scenario.exp-930.geoeng.cld.artificial.iter4_monthly_20y_nf_80yrs.bin'
file_x1_1 = constants.output_folder()+'/scenario.exp-930.geoeng.cld.artificial.frominput_x1.1_80yrs.bin'

lats_india=(8,33)
lons_india=(69,85)
lats_china=(24,45)
lons_china=(80,120)
lats_aus=(12,38)
lons_aus=(114,153)
# 'CLOUDS'
cld_base = data_from_binary(constants.cloud_def_file())['cloud']
cld_best = data_from_binary(constants.cloud_folder()+
                        '/cld.artificial.iter18_monthly_20y_nf.ctl')['cloud']
cld_iter4 = data_from_binary(constants.cloud_folder()+
                        '/cld.artificial.iter4_monthly_20y_nf.ctl')['cloud']
cld_x1_1 = data_from_binary(constants.cloud_folder()+
                        '/cld.artificial.frominput_x1.1.ctl')['cloud']

cld_base_gm = cld_base.mean(axis=-1).mean(axis=-1)
cld_best_gm = cld_best.mean(axis=-1).mean(axis=-1)
cld_iter4_gm = cld_iter4.mean(axis=-1).mean(axis=-1)
cld_x1_1_gm = cld_x1_1.mean(axis=-1).mean(axis=-1)

# 'TSURF'
ts_ctl = to_celsus(data_from_binary(file_control)['tsurf'])
ts_base = to_celsus(data_from_binary(file_baseline)['tsurf']).reshape(80,12,48,96)
ts_best = to_celsus(data_from_binary(file_best)['tsurf']).reshape(80,12,48,96)
ts_iter4 = to_celsus(data_from_binary(file_4th_iter)['tsurf']).reshape(80,12,48,96)
ts_x1_1 = to_celsus(data_from_binary(file_x1_1)['tsurf']).reshape(80,12,48,96)

ts_ctl_gm=ts_ctl.mean()
ts_base_gm=np.insert(ts_base.mean(axis=-1).mean(axis=-1).mean(axis=-1),0,ts_ctl_gm)
ts_best_gm=np.insert(ts_best.mean(axis=-1).mean(axis=-1).mean(axis=-1),0,ts_ctl_gm)
ts_iter4_gm=np.insert(ts_iter4.mean(axis=-1).mean(axis=-1).mean(axis=-1),0,ts_ctl_gm)
ts_x1_1_gm=np.insert(ts_x1_1.mean(axis=-1).mean(axis=-1).mean(axis=-1),0,ts_ctl_gm)

ts_base_anom_jja_70s = mean_70s((ts_base-ts_ctl)[:,5:8,...].mean(axis=1))
ts_base_anom_djf_70s = mean_70s((ts_base-ts_ctl)[:,[0,1,-1],...].mean(axis=1))
ts_best_anom_jja_70s = mean_70s((ts_best-ts_ctl)[:,5:8,...].mean(axis=1))
ts_best_anom_djf_70s = mean_70s((ts_best-ts_ctl)[:,[0,1,-1],...].mean(axis=1))

ts_base_std=(ts_base-ts_ctl).std(axis=1)
ts_best_anom_jja_stdunit = (ts_best-ts_ctl)[:,5:8,...].mean(axis=1)/ts_base_std
ts_iter4_anom_jja_stdunit = (ts_iter4-ts_ctl)[:,5:8,...].mean(axis=1)/ts_base_std
ts_x1_1_anom_jja_stdunit = (ts_x1_1-ts_ctl)[:,5:8,...].mean(axis=1)/ts_base_std

ts_best_anom_jja_stdunit_20s = mean_20s(ts_best_anom_jja_stdunit)
ts_best_anom_jja_stdunit_70s = mean_70s(ts_best_anom_jja_stdunit)
ts_iter4_anom_jja_stdunit_20s = mean_20s(ts_iter4_anom_jja_stdunit)
ts_iter4_anom_jja_stdunit_70s = mean_70s(ts_iter4_anom_jja_stdunit)
ts_x1_1_anom_jja_stdunit_20s = mean_20s(ts_x1_1_anom_jja_stdunit)
ts_x1_1_anom_jja_stdunit_70s = mean_70s(ts_x1_1_anom_jja_stdunit)

# India
ts_best_anom_jja_stdunit_20s_india = to_regional_mean(ts_best_anom_jja_stdunit_20s,lats_india,lons_india)
ts_iter4_anom_jja_stdunit_20s_india = to_regional_mean(ts_iter4_anom_jja_stdunit_20s,lats_india,lons_india)
ts_x1_1_anom_jja_stdunit_20s_india = to_regional_mean(ts_x1_1_anom_jja_stdunit_20s,lats_india,lons_india)
ts_best_anom_jja_stdunit_70s_india = to_regional_mean(ts_best_anom_jja_stdunit_70s,lats_india,lons_india)
ts_iter4_anom_jja_stdunit_70s_india = to_regional_mean(ts_iter4_anom_jja_stdunit_70s,lats_india,lons_india)
ts_x1_1_anom_jja_stdunit_70s_india = to_regional_mean(ts_x1_1_anom_jja_stdunit_70s,lats_india,lons_india)

# China
ts_best_anom_jja_stdunit_20s_china = to_regional_mean(ts_best_anom_jja_stdunit_20s,lats_china,lons_china)
ts_iter4_anom_jja_stdunit_20s_china = to_regional_mean(ts_iter4_anom_jja_stdunit_20s,lats_china,lons_china)
ts_x1_1_anom_jja_stdunit_20s_china = to_regional_mean(ts_x1_1_anom_jja_stdunit_20s,lats_china,lons_china)
ts_best_anom_jja_stdunit_70s_china = to_regional_mean(ts_best_anom_jja_stdunit_70s,lats_china,lons_china)
ts_iter4_anom_jja_stdunit_70s_china = to_regional_mean(ts_iter4_anom_jja_stdunit_70s,lats_china,lons_china)
ts_x1_1_anom_jja_stdunit_70s_china = to_regional_mean(ts_x1_1_anom_jja_stdunit_70s,lats_china,lons_china)

# Australia
ts_best_anom_jja_stdunit_20s_aus = to_regional_mean(ts_best_anom_jja_stdunit_20s,lats_aus,lons_aus)
ts_iter4_anom_jja_stdunit_20s_aus = to_regional_mean(ts_iter4_anom_jja_stdunit_20s,lats_aus,lons_aus)
ts_x1_1_anom_jja_stdunit_20s_aus = to_regional_mean(ts_x1_1_anom_jja_stdunit_20s,lats_aus,lons_aus)
ts_best_anom_jja_stdunit_70s_aus = to_regional_mean(ts_best_anom_jja_stdunit_70s,lats_aus,lons_aus)
ts_iter4_anom_jja_stdunit_70s_aus = to_regional_mean(ts_iter4_anom_jja_stdunit_70s,lats_aus,lons_aus)
ts_x1_1_anom_jja_stdunit_70s_aus = to_regional_mean(ts_x1_1_anom_jja_stdunit_70s,lats_aus,lons_aus)

# //==========================================================================//
# //==========================================================================//
# //==========================================================================//

# 'PRECIP'
p_ctl = data_from_binary(file_control)['precip']*-86400
p_base = data_from_binary(file_baseline)['precip'].reshape(80,12,48,96)*-86400
p_best = data_from_binary(file_best)['precip'].reshape(80,12,48,96)*-86400
p_iter4 = data_from_binary(file_4th_iter)['precip'].reshape(80,12,48,96)*-86400
p_x1_1 = data_from_binary(file_x1_1)['precip'].reshape(80,12,48,96)*-86400

p_ctl_gm=p_ctl.mean()
p_base_gm=np.insert(p_base.mean(axis=-1).mean(axis=-1).mean(axis=-1),0,p_ctl_gm)
p_best_gm=np.insert(p_best.mean(axis=-1).mean(axis=-1).mean(axis=-1),0,p_ctl_gm)
p_iter4_gm=np.insert(p_iter4.mean(axis=-1).mean(axis=-1).mean(axis=-1),0,p_ctl_gm)
p_x1_1_gm=np.insert(p_x1_1.mean(axis=-1).mean(axis=-1).mean(axis=-1),0,p_ctl_gm)

p_base_anom_jja_70s = mean_70s((p_base-p_ctl)[:,5:8,...].mean(axis=1))
p_base_anom_djf_70s = mean_70s((p_base-p_ctl)[:,[0,1,-1],...].mean(axis=1))
p_best_anom_jja_70s = mean_70s((p_best-p_ctl)[:,5:8,...].mean(axis=1))
p_best_anom_djf_70s = mean_70s((p_best-p_ctl)[:,[0,1,-1],...].mean(axis=1))

p_base_std=(p_base-p_ctl).std(axis=1)
p_best_anom_jja_stdunit = (p_best-p_ctl)[:,5:8,...].mean(axis=1)/p_base_std
p_iter4_anom_jja_stdunit = (p_iter4-p_ctl)[:,5:8,...].mean(axis=1)/p_base_std
p_x1_1_anom_jja_stdunit = (p_x1_1-p_ctl)[:,5:8,...].mean(axis=1)/p_base_std

p_best_anom_jja_stdunit_20s = mean_20s(p_best_anom_jja_stdunit)
p_best_anom_jja_stdunit_70s = mean_70s(p_best_anom_jja_stdunit)
p_iter4_anom_jja_stdunit_20s = mean_20s(p_iter4_anom_jja_stdunit)
p_iter4_anom_jja_stdunit_70s = mean_70s(p_iter4_anom_jja_stdunit)
p_x1_1_anom_jja_stdunit_20s = mean_20s(p_x1_1_anom_jja_stdunit)
p_x1_1_anom_jja_stdunit_70s = mean_70s(p_x1_1_anom_jja_stdunit)

# India
p_best_anom_jja_stdunit_20s_india = to_regional_mean(p_best_anom_jja_stdunit_20s,lats_india,lons_india)
p_iter4_anom_jja_stdunit_20s_india = to_regional_mean(p_iter4_anom_jja_stdunit_20s,lats_india,lons_india)
p_x1_1_anom_jja_stdunit_20s_india = to_regional_mean(p_x1_1_anom_jja_stdunit_20s,lats_india,lons_india)
p_best_anom_jja_stdunit_70s_india = to_regional_mean(p_best_anom_jja_stdunit_70s,lats_india,lons_india)
p_iter4_anom_jja_stdunit_70s_india = to_regional_mean(p_iter4_anom_jja_stdunit_70s,lats_india,lons_india)
p_x1_1_anom_jja_stdunit_70s_india = to_regional_mean(p_x1_1_anom_jja_stdunit_70s,lats_india,lons_india)

# China
p_best_anom_jja_stdunit_20s_china = to_regional_mean(p_best_anom_jja_stdunit_20s,lats_china,lons_china)
p_iter4_anom_jja_stdunit_20s_china = to_regional_mean(p_iter4_anom_jja_stdunit_20s,lats_china,lons_china)
p_x1_1_anom_jja_stdunit_20s_china = to_regional_mean(p_x1_1_anom_jja_stdunit_20s,lats_china,lons_china)
p_best_anom_jja_stdunit_70s_china = to_regional_mean(p_best_anom_jja_stdunit_70s,lats_china,lons_china)
p_iter4_anom_jja_stdunit_70s_china = to_regional_mean(p_iter4_anom_jja_stdunit_70s,lats_china,lons_china)
p_x1_1_anom_jja_stdunit_70s_china = to_regional_mean(p_x1_1_anom_jja_stdunit_70s,lats_china,lons_china)

# Australia
p_best_anom_jja_stdunit_20s_aus = to_regional_mean(p_best_anom_jja_stdunit_20s,lats_aus,lons_aus)
p_iter4_anom_jja_stdunit_20s_aus = to_regional_mean(p_iter4_anom_jja_stdunit_20s,lats_aus,lons_aus)
p_x1_1_anom_jja_stdunit_20s_aus = to_regional_mean(p_x1_1_anom_jja_stdunit_20s,lats_aus,lons_aus)
p_best_anom_jja_stdunit_70s_aus = to_regional_mean(p_best_anom_jja_stdunit_70s,lats_aus,lons_aus)
p_iter4_anom_jja_stdunit_70s_aus = to_regional_mean(p_iter4_anom_jja_stdunit_70s,lats_aus,lons_aus)
p_x1_1_anom_jja_stdunit_70s_aus = to_regional_mean(p_x1_1_anom_jja_stdunit_70s,lats_aus,lons_aus)

# //==========================================================================//
# //==========================================================================//
# //==========================================================================//

#PLOT
plot_cloud()
plt.savefig(dsk+'clouds.png', bbox_inches='tight',dpi=300)

plot_tsurf()
plt.savefig(dsk+'tsurf.png', bbox_inches='tight',dpi=300)

plot_precip()
plt.savefig(dsk+'precip.png', bbox_inches='tight',dpi=300)

plot_std()
plt.savefig(dsk+'std.png', bbox_inches='tight',dpi=300)

# TSURF MAPS
cmaplev = np.arange(-2.5,17.5+0.1,0.1)
cbticks = np.arange(-2.5,17.5+2.5,2.5)
cmap = cm.rainbow
def_cube=cube_from_data(ts_base_anom_jja_70s, var_name=  'tsurf_base_jja', units = '°C', latitude = constants.lat(), longitude=constants.lon())
plot_param.from_cube(def_cube,tit='',cmaplev=cmaplev,cmap=cmap,
        cbticks=cbticks).plot(projection=None,statistics=0,outpath=dsk)

def_cube=cube_from_data(ts_base_anom_djf_70s, var_name=  'tsurf_base_djf', units = '°C', latitude = constants.lat(), longitude=constants.lon())
plot_param.from_cube(def_cube,tit='',cmaplev=cmaplev,cmap=cmap,
        cbticks=cbticks).plot(projection=None,statistics=0,outpath=dsk)

def_cube=cube_from_data(ts_best_anom_jja_70s, var_name=  'tsurf_best_jja', units = '°C', latitude = constants.lat(), longitude=constants.lon())
plot_param.from_cube(def_cube,tit='',cmaplev=cmaplev,cmap=cmap,
        cbticks=cbticks).plot(projection=None,statistics=0,outpath=dsk)

def_cube=cube_from_data(ts_best_anom_djf_70s, var_name=  'tsurf_best_djf', units = '°C', latitude = constants.lat(), longitude=constants.lon())
plot_param.from_cube(def_cube,tit='',cmaplev=cmaplev,cmap=cmap,
        cbticks=cbticks).plot(projection=None,statistics=0,outpath=dsk)

def_cube=cube_from_data(ts_base_anom_djf_70s-ts_best_anom_djf_70s, var_name=  'tsurf_base-best_djf', units = '°C', latitude = constants.lat(), longitude=constants.lon())
plot_param.from_cube(def_cube,tit='',cmaplev=cmaplev,cmap=cmap,
        cbticks=cbticks).plot(projection=None,statistics=0,outpath=dsk)

def_cube=cube_from_data(ts_base_anom_jja_70s-ts_best_anom_jja_70s, var_name=  'tsurf_base-best_jja', units = '°C', latitude = constants.lat(), longitude=constants.lon())
plot_param.from_cube(def_cube,tit='',cmaplev=cmaplev,cmap=cmap,
        cbticks=cbticks).plot(projection=None,statistics=0,outpath=dsk)

# PRECIP MAPS
cmaplev = np.arange(-5,5+0.01,0.01)
cbticks = np.arange(-5,5+1,1)
cmap=cm.BrBG
def_cube=cube_from_data(p_base_anom_jja_70s, var_name=  'precip_base_jja', units = 'mm/d', latitude = constants.lat(), longitude=constants.lon())
plot_param.from_cube(def_cube,tit='',cmaplev=cmaplev,cmap=cmap,
        cbticks=cbticks).plot(projection=None,statistics=0,outpath=dsk)

def_cube=cube_from_data(p_base_anom_djf_70s, var_name=  'precip_base_djf', units = 'mm/d', latitude = constants.lat(), longitude=constants.lon())
plot_param.from_cube(def_cube,tit='',cmaplev=cmaplev,cmap=cmap,
        cbticks=cbticks).plot(projection=None,statistics=0,outpath=dsk)

def_cube=cube_from_data(p_best_anom_jja_70s, var_name=  'precip_best_jja', units = 'mm/d', latitude = constants.lat(), longitude=constants.lon())
plot_param.from_cube(def_cube,tit='',cmaplev=cmaplev,cmap=cmap,
        cbticks=cbticks).plot(projection=None,statistics=0,outpath=dsk)

def_cube=cube_from_data(p_best_anom_djf_70s, var_name=  'precip_best_djf', units = 'mm/d', latitude = constants.lat(), longitude=constants.lon())
plot_param.from_cube(def_cube,tit='',cmaplev=cmaplev,cmap=cmap,
        cbticks=cbticks).plot(projection=None,statistics=0,outpath=dsk)

def_cube=cube_from_data(p_base_anom_djf_70s-p_best_anom_djf_70s, var_name=  'precip_base-best_djf', units = 'mm/d', latitude = constants.lat(), longitude=constants.lon())
plot_param.from_cube(def_cube,tit='',cmaplev=cmaplev,cmap=cmap,
        cbticks=cbticks).plot(projection=None,statistics=0,outpath=dsk)

def_cube=cube_from_data(p_base_anom_jja_70s-p_best_anom_jja_70s, var_name=  'precip_base-best_jja', units = 'mm/d', latitude = constants.lat(), longitude=constants.lon())
plot_param.from_cube(def_cube,tit='',cmaplev=cmaplev,cmap=cmap,
        cbticks=cbticks).plot(projection=None,statistics=0,outpath=dsk)


def_cube=cube_from_data(ts_best_anom_jja_stdunit_70s, var_name=  'tsurf_best_jja_stdunit', units = '°C', latitude = constants.lat(), longitude=constants.lon())
mycmap=custom_cmap(cm.Blues_r,cm.Reds)
plot_param.from_cube(def_cube,tit='temperature anomaly JJA 70s',cmaplev=np.arange(-5,5+0.1,0.1),cmap=mycmap, units='baseline std',
        cbticks=np.arange(-5,5+1,1)).plot(projection=None,statistics=0,outpath=dsk)

def_cube=cube_from_data(p_best_anom_jja_stdunit_70s, var_name=  'precip_best_jja_stdunit', units = 'mm/d', latitude = constants.lat(), longitude=constants.lon())
mycmap=custom_cmap(cm.pink,cm.Blues)
plot_param.from_cube(def_cube,tit='precipitation anomaly JJA 70s',cmaplev=np.arange(-5,5+0.1,0.1),cmap=mycmap, units='baseline std',
        cbticks=np.arange(-5,5+1,1)).plot(projection=None,statistics=0,outpath=dsk)
