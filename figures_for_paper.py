from myfuncs import *
import matplotlib

r_cld=from_binary('r_calibration').r
data_filename=os.path.join(constants.output_folder(),
                 'scenario.exp-930.geoeng.cld.artificial.iter20_50yrs')
data=from_binary(data_filename)[['tsurf','precip']]
anomalies=data.anomalies()

# ============================================================== #
# FIG 1) r_cld annual mean + seasonal means (JJA & DJF)

def plot_fig1(constrained_layout=False):
    matplotlib.rcParams.update({'font.size': 14})
    fig1 = plt.figure(figsize=(16,9))
    heights = [5,5,1]
    gs=fig1.add_gridspec(ncols=2, nrows=3,
                         height_ratios=heights,
                         wspace=0.015, hspace=0.3)
    f1_ax1 = fig1.add_subplot(gs[0, 0],projection=ccrs.Robinson())
    im=r_cld.annual_mean().plotvar(ax=f1_ax1,
                                statistics=False,
                                add_colorbar=False,
                                levels=np.arange(-9,0+0.2,0.2),
                                cmap=cm.viridis,
                                title='r_cld Annual Mean')
    f1_ax2 = fig1.add_subplot(gs[0, 1],projection=ccrs.Robinson())
    r_cld.seasonal_cycle().plotvar(ax=f1_ax2,
                                statistics=False,
                                add_colorbar=False,
                                levels=np.arange(-9,0+0.2,0.2),
                                cmap=cm.viridis,
                                title='r_cld Seasonal Cycle (DJF-JJA)')
    f1_ax3 = fig1.add_subplot(gs[1, 0],projection=ccrs.Robinson())
    r_cld.group_by('season').sel(time='DJF').plotvar(ax=f1_ax3,
                                statistics=False,
                                add_colorbar=False,
                                levels=np.arange(-9,0+0.2,0.2),
                                cmap=cm.viridis,
                                title='r_cld DJF')
    f1_ax4 = fig1.add_subplot(gs[1, 1],projection=ccrs.Robinson())
    r_cld.group_by('season').sel(time='JJA').plotvar(ax=f1_ax4,
                                statistics=False,
                                add_colorbar=False,
                                levels=np.arange(-9,0+0.2,0.2),
                                cmap=cm.viridis,
                                title='r_cld JJA')
    f1_ax5 = fig1.add_subplot(gs[2, :])
    plt.colorbar(im,cax=f1_ax5,
                 orientation='horizontal')

# ============================================================== #
# FIG 2) Annual mean, seasonal cycle and global mean anomalies



# ============================================================== #
# ============================================================== #
# ============================================================== #

plot_fig1()
