import warnings
warnings.filterwarnings("ignore")
from myfuncs import *
import matplotlib
import matplotlib.colors as colors
from matplotlib.ticker import AutoMinorLocator,FormatStrFormatter

r_cld=from_binary('r_calibration').r
srm_filename=os.path.join(constants.output_folder(),
                 'scenario.exp-930.geoeng.cld.artificial.iter20_50yrs')
CO2x2_filename=os.path.join(constants.scenario_2xCO2())
homogeneous_filename=os.path.join(constants.output_folder(),'scenario.exp-930.geoeng.cld.artificial.frominput_x1.085_50yrs')
cloud_srm_filename=constants.get_art_forcing_filename(srm_filename,
                output_path= constants.cloud_folder()+'/cld.artificial.iteration')
control=from_binary(constants.control_def_file())[['tsurf','precip']]
srm=from_binary(srm_filename)[['tsurf','precip']]
CO2x2=from_binary(CO2x2_filename)[['tsurf','precip']]
homogeneous=from_binary(homogeneous_filename)[['tsurf','precip']]
cloud_srm=from_binary(cloud_srm_filename).cloud
cloud_CO2x2=from_binary(constants.cloud_def_file()).cloud
cloud_homogeneous=from_binary(os.path.join(constants.cloud_folder(),'cld.artificial.frominput_x1.085')).cloud
tsurf=srm.anomalies().tsurf
precip=srm.anomalies().precip

# (cloud.annual_mean().global_mean()/from_binary(constants.cloud_def_file()).cloud.annual_mean().global_mean())
# (tsurf.annual_mean().srex_mean()<=0.3).sum()/26
# (precip.annual_mean().srex_mean()<=0.01).sum()/26

gm0=control.global_mean().to_celsius().mean()
gm=srm.global_mean().to_celsius().group_by('year')

cm0=cm.Spectral_r
col1=cm0(np.linspace(0,0.4,102))
w1=np.array(list(map(lambda x: np.linspace(x,1,26),col1[-1]))).transpose()
col2=cm0(np.linspace(0.6,1,102))
w2=np.array(list(map(lambda x: np.linspace(1,x,26),col2[0]))).transpose()
cols1=np.vstack([col1,w1,w2,col2])
my_cmap1 = colors.LinearSegmentedColormap.from_list('my_colormap', cols1)

# ============================================================== #
# FIG 1) Annual mean anomalies
def plot_fig1():
    matplotlib.rcParams.update({'font.size': 14})
    fig1 = plt.figure(figsize=(16,9),constrained_layout=False)
    heights = [10,1]
    wspace=0.15; hspace=0.1; ncols=3; nrows=2
    gs1=fig1.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         top=0.97,bottom=0.72)
    gs2=fig1.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         top=0.625,bottom=0.375)
    gs3=fig1.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         top=0.28,bottom=0.03)

    f1_ax1 = fig1.add_subplot(gs1[0, 0],projection=ccrs.Robinson())
    im=CO2x2.anomalies().tsurf.annual_mean().plotvar(ax=f1_ax1,
                                   levels=np.arange(1,5+0.02,0.02),
                                   cmap=cm.YlOrRd,
                                   add_colorbar=False,
                                   title='Abrupt2xCO2 tsurf')
    f1_ax2 = fig1.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    im2=homogeneous.anomalies().tsurf.annual_mean().plotvar(ax=f1_ax2,
                                   levels=np.arange(-1,2+0.01,0.01),
                                   norm=colors.DivergingNorm(vmin=-1, vcenter=0., vmax=2+0.01),
                                   cmap=my_cmap1,
                                   add_colorbar=False,
                                   title='Homogeneous tsurf')
    f1_ax3 = fig1.add_subplot(gs1[0, 2],projection=ccrs.Robinson())
    im3=srm.anomalies().tsurf.annual_mean().plotvar(ax=f1_ax3,
                                   levels=np.arange(-0.1,0.5+0.002,0.002),
                                   norm=colors.DivergingNorm(vmin=-0.1, vcenter=0., vmax=0.5+0.002),
                                   cmap=my_cmap1,
                                   add_colorbar=False,
                                   title='SRM tsurf')

    f1_ax4 = fig1.add_subplot(gs1[1, 0])
    plt.colorbar(im,cax=f1_ax4, orientation='horizontal',label='K',
                 ticks=np.arange(1,5+0.5,0.5))
    f1_ax5 = fig1.add_subplot(gs1[1, 1])
    plt.colorbar(im2,cax=f1_ax5, orientation='horizontal',label='K',
                 ticks=np.arange(-1,2+0.5,0.5))
    f1_ax6 = fig1.add_subplot(gs1[1, 2])
    plt.colorbar(im3,cax=f1_ax6, orientation='horizontal',label='K',
                 ticks=np.arange(-0.1,0.5+0.1,0.1))

    f1_ax7 = fig1.add_subplot(gs2[0, 0],projection=ccrs.Robinson())
    im=CO2x2.anomalies().precip.annual_mean().plotvar(ax=f1_ax7,
                                   levels=np.arange(0,1.5+0.02,0.02),
                                   cmap=cm.YlOrRd,
                                   add_colorbar=False,
                                   title='Abrupt2xCO2 precip')
    f1_ax8 = fig1.add_subplot(gs2[0, 1],projection=ccrs.Robinson())
    im2=homogeneous.anomalies().precip.annual_mean().plotvar(ax=f1_ax8,
                                   levels=np.arange(-0.5,0.2+0.005,0.005),
                                   norm=colors.DivergingNorm(vmin=-0.5, vcenter=0, vmax=0.2+0.005),
                                   cmap=my_cmap1,
                                   add_colorbar=False,
                                   title='Homogeneous precip')
    f1_ax9 = fig1.add_subplot(gs2[0, 2],projection=ccrs.Robinson())
    im3=srm.anomalies().precip.annual_mean().plotvar(ax=f1_ax9,
                                   levels=np.arange(-0.01,0.03+0.0001,0.0001),
                                   norm=colors.DivergingNorm(vmin=-0.01, vcenter=0., vmax=0.03+0.0001),
                                   cmap=my_cmap1,
                                   add_colorbar=False,
                                   title='SRM precip')

    f1_ax10 = fig1.add_subplot(gs2[1, 0])
    plt.colorbar(im,cax=f1_ax10, orientation='horizontal',label='mm/day',
                 ticks=np.arange(0,1.5+0.25,0.25))
    f1_ax11 = fig1.add_subplot(gs2[1, 1])
    plt.colorbar(im2,cax=f1_ax11, orientation='horizontal',label='mm/day',
                 ticks=np.arange(-0.5,0.2+0.1,0.1))
    f1_ax12 = fig1.add_subplot(gs2[1, 2])
    plt.colorbar(im3,cax=f1_ax12, orientation='horizontal',label='mm/day',
                 ticks=np.arange(-0.01,0.03+0.01,0.01))

    f1_ax13 = fig1.add_subplot(gs3[0, 0],projection=ccrs.Robinson())
    im=cloud_CO2x2.annual_mean().plotvar(ax=f1_ax13,
                                   levels=np.arange(0,1+0.01,0.01),
                                   add_colorbar=False,
                                   title='Abrupt2xCO2 cloud')
    f1_ax14 = fig1.add_subplot(gs3[0, 1],projection=ccrs.Robinson())
    im2=(cloud_homogeneous.anomalies()).annual_mean().plotvar(ax=f1_ax14,
                                    levels=np.arange(0.01,0.1+0.001,0.001),
                                    cmap=cm.YlOrRd,
                                    add_colorbar=False,
                                    coast_kwargs={'edgecolor':'k'})
    f1_ax14.set_title('<Homogeneous> - <Abrupt2xCO2> cloud',fontsize=11)
    f1_ax15 = fig1.add_subplot(gs3[0, 2],projection=ccrs.Robinson())
    im3=(cloud_srm.anomalies()).annual_mean().plotvar(ax=f1_ax15,
                                    levels=np.arange(-0.04,0.13+0.001,0.001),
                                    norm=colors.DivergingNorm(vmin=-0.04, vcenter=0., vmax=0.13+0.001),
                                    cmap=my_cmap1,
                                    add_colorbar=False,
                                    coast_kwargs={'edgecolor':'k'})
    f1_ax15.set_title('<SRM> - <Abrupt2xCO2> cloud',fontsize=11)

    f1_ax16 = fig1.add_subplot(gs3[1, 0])
    plt.colorbar(im,cax=f1_ax16, orientation='horizontal',
                 ticks=np.arange(0,1+0.2,0.2))
    f1_ax17 = fig1.add_subplot(gs3[1, 1])
    plt.colorbar(im2,cax=f1_ax17, orientation='horizontal',
                 ticks=np.arange(0.01,0.1+0.02,0.02))
    f1_ax18 = fig1.add_subplot(gs3[1, 2])
    plt.colorbar(im3,cax=f1_ax18, orientation='horizontal',
                 ticks=np.arange(-0.04,0.13+0.04,0.04))


def plot_fig1_bis():
    matplotlib.rcParams.update({'font.size': 14})
    fig1 = plt.figure(figsize=(16,9),constrained_layout=False)
    heights = [10,1]
    wspace=0.15; hspace=0.1; ncols=3; nrows=2
    gs1=fig1.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         top=0.97,bottom=0.72)
    gs2=fig1.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         top=0.625,bottom=0.375)
    gs3=fig1.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         top=0.28,bottom=0.03)

    f1_ax1 = fig1.add_subplot(gs1[0, 0],projection=ccrs.Robinson())
    im=CO2x2.anomalies().tsurf.annual_mean().plotvar(ax=f1_ax1,
                                   levels=np.arange(1,5+0.02,0.02),
                                   cmap=cm.YlOrRd,
                                   add_colorbar=False,
                                   title='Abrupt2xCO2 tsurf')
    f1_ax2 = fig1.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    im2=homogeneous.anomalies().tsurf.annual_mean().plotvar(ax=f1_ax2,
                                   levels=np.arange(-1,2+0.01,0.01),
                                   norm=colors.DivergingNorm(vmin=-1, vcenter=0., vmax=2+0.01),
                                   cmap=my_cmap1,
                                   add_colorbar=False,
                                   title='Homogeneous tsurf')
    f1_ax3 = fig1.add_subplot(gs1[0, 2],projection=ccrs.Robinson())
    im3=srm.anomalies().tsurf.annual_mean().plotvar(ax=f1_ax3,
                                   levels=np.arange(-1,2+0.01,0.01),
                                   norm=colors.DivergingNorm(vmin=-1, vcenter=0., vmax=2+0.01),
                                   cmap=my_cmap1,
                                   add_colorbar=False,
                                   title='SRM tsurf')

    f1_ax4 = fig1.add_subplot(gs1[1, 0])
    plt.colorbar(im,cax=f1_ax4, orientation='horizontal',label='K',
                 ticks=np.arange(1,5+0.5,0.5))
    f1_ax5 = fig1.add_subplot(gs1[1, 1:])
    plt.colorbar(im2,cax=f1_ax5, orientation='horizontal',label='K',
                 ticks=np.arange(-1,2+0.5,0.5))
    # f1_ax6 = fig1.add_subplot(gs1[1, 2])
    # plt.colorbar(im3,cax=f1_ax6, orientation='horizontal',label='K',
    #              ticks=np.arange(-0.1,0.5+0.1,0.1))

    f1_ax7 = fig1.add_subplot(gs2[0, 0],projection=ccrs.Robinson())
    im=CO2x2.anomalies().precip.annual_mean().plotvar(ax=f1_ax7,
                                   levels=np.arange(0,1.5+0.02,0.02),
                                   cmap=cm.YlOrRd,
                                   add_colorbar=False,
                                   title='Abrupt2xCO2 precip')
    f1_ax8 = fig1.add_subplot(gs2[0, 1],projection=ccrs.Robinson())
    min,max,step=-0.4,0.1,0.005
    im2=homogeneous.anomalies().precip.annual_mean().plotvar(ax=f1_ax8,
                                   levels=np.arange(min,max+step,step),
                                   norm=colors.DivergingNorm(vmin=min, vcenter=0, vmax=max+step),
                                   cmap=my_cmap1,
                                   add_colorbar=False,
                                   title='Homogeneous precip')
    f1_ax9 = fig1.add_subplot(gs2[0, 2],projection=ccrs.Robinson())
    im3=srm.anomalies().precip.annual_mean().plotvar(ax=f1_ax9,
                                   levels=np.arange(min,max+step,step),
                                   norm=colors.DivergingNorm(vmin=min, vcenter=0, vmax=max+step),
                                   cmap=my_cmap1,
                                   add_colorbar=False,
                                   title='SRM precip')

    f1_ax10 = fig1.add_subplot(gs2[1, 0])
    plt.colorbar(im,cax=f1_ax10, orientation='horizontal',label='mm/day',
                 ticks=np.arange(0,1.5+0.25,0.25))
    f1_ax11 = fig1.add_subplot(gs2[1, 1:])
    plt.colorbar(im2,cax=f1_ax11, orientation='horizontal',label='mm/day',
                 ticks=np.arange(min,max+0.1,0.1))
    # f1_ax12 = fig1.add_subplot(gs2[1, 2])
    # plt.colorbar(im3,cax=f1_ax12, orientation='horizontal',label='mm/day',
    #              ticks=np.arange(-0.01,0.03+0.01,0.01))

    f1_ax13 = fig1.add_subplot(gs3[0, 0],projection=ccrs.Robinson())
    im=cloud_CO2x2.annual_mean().plotvar(ax=f1_ax13,
                                   levels=np.arange(0,1+0.01,0.01),
                                   add_colorbar=False,
                                   title='Abrupt2xCO2 cloud')
    f1_ax14 = fig1.add_subplot(gs3[0, 1],projection=ccrs.Robinson())
    min,max,step=-0.04,0.13,0.001
    im2=(cloud_homogeneous.anomalies()).annual_mean().plotvar(ax=f1_ax14,
                                    levels=np.arange(min,max+step,step),
                                    norm=colors.DivergingNorm(vmin=min, vcenter=0, vmax=max+step),
                                    cmap=my_cmap1,
                                    add_colorbar=False,
                                    coast_kwargs={'edgecolor':'k'})
    f1_ax14.set_title('<Homogeneous> - <Abrupt2xCO2> cloud',fontsize=11)
    f1_ax15 = fig1.add_subplot(gs3[0, 2],projection=ccrs.Robinson())
    im3=(cloud_srm.anomalies()).annual_mean().plotvar(ax=f1_ax15,
                                    levels=np.arange(min,max+step,step),
                                    norm=colors.DivergingNorm(vmin=min, vcenter=0, vmax=max+step),
                                    cmap=my_cmap1,
                                    add_colorbar=False,
                                    coast_kwargs={'edgecolor':'k'})
    f1_ax15.set_title('<SRM> - <Abrupt2xCO2> cloud',fontsize=11)

    f1_ax16 = fig1.add_subplot(gs3[1, 0])
    plt.colorbar(im,cax=f1_ax16, orientation='horizontal',
                 ticks=np.arange(0,1+0.2,0.2))
    # f1_ax17 = fig1.add_subplot(gs3[1, 1])
    # plt.colorbar(im2,cax=f1_ax17, orientation='horizontal',
    #              ticks=np.arange(0.01,0.1+0.02,0.02))
    f1_ax18 = fig1.add_subplot(gs3[1, 1:])
    plt.colorbar(im3,cax=f1_ax18, orientation='horizontal',
                 ticks=np.arange(min,max+0.04,0.04))

plot_fig1_bis()

# ============================================================== #
# FIG 2) r_cld annual mean + seasonal means (JJA & DJF)
def plot_fig2():
    matplotlib.rcParams.update({'font.size': 14})
    fig2 = plt.figure(figsize=(16,9),constrained_layout=False)
    heights = [10,1]
    wspace=0.15; hspace=0.2; ncols=2; nrows=2
    gs1=fig2.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         top=0.95,bottom=0.55)
    gs2=fig2.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         top=0.45,bottom=0.05)
    min,max,step=-9,3,0.2
    f2_ax1 = fig2.add_subplot(gs1[0, 0],projection=ccrs.Robinson())
    im=r_cld.annual_mean().plotvar(ax=f2_ax1,
                                statistics=False,
                                add_colorbar=False,
                                levels=np.arange(-9,0+0.2,0.2),
                                cmap=cm.viridis,
                                title='r_cld Annual Mean')
    f2_ax2 = fig2.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    im2=r_cld.seasonal_cycle().plotvar(ax=f2_ax2,
                                statistics=False,
                                add_colorbar=False,
                                levels=np.arange(-4,5+0.2,0.2),
                                cmap=cm.viridis,
                                title='r_cld Seasonal Cycle')
    f2_ax3 = fig2.add_subplot(gs1[1, 0])
    plt.colorbar(im,cax=f2_ax3, orientation='horizontal')
    f2_ax4 = fig2.add_subplot(gs1[1, 1])
    plt.colorbar(im2,cax=f2_ax4, orientation='horizontal',
                 ticks=np.arange(-4,5+1,1))

    f2_ax5 = fig2.add_subplot(gs2[0, 0],projection=ccrs.Robinson())
    r_cld.group_by('season').sel(time='DJF').plotvar(ax=f2_ax5,
                                statistics=False,
                                add_colorbar=False,
                                levels=np.arange(-9,3+0.2,0.2),
                                cmap=cm.viridis,
                                title='r_cld DJF')
    f2_ax6 = fig2.add_subplot(gs2[0, 1],projection=ccrs.Robinson())
    r_cld.group_by('season').sel(time='JJA').plotvar(ax=f2_ax6,
                                statistics=False,
                                add_colorbar=False,
                                levels=np.arange(-9,3+0.2,0.2),
                                cmap=cm.viridis,
                                title='r_cld JJA')
    f2_ax7 = fig2.add_subplot(gs2[1, :])
    plt.colorbar(im,cax=f2_ax7,
                 orientation='horizontal')

# ============================================================== #
# FIG 3) anomalies averaged over SREX regions
def plot_fig3():
    matplotlib.rcParams.update({'font.size': 14})
    fig3 = plt.figure(figsize=(16,9))
    gs=fig3.add_gridspec(ncols=1, nrows=2,hspace=0.1)
    f3_ax1 = fig3.add_subplot(gs[0,0])
    tsurf.annual_mean().srex_mean().plot(ax=f3_ax1,marker='x',linestyle='',markeredgewidth=2)
    plt.title('')
    plt.xlim(0,27)
    plt.ylim(-0.1,0.5)
    plt.hlines(0,*plt.xlim(),linestyles='solid',linewidth=0.5)
    plt.xticks(np.arange(1,27))
    plt.xlabel('')
    f3_ax1.set_xticklabels([])
    f3_ax1.yaxis.set_minor_locator(AutoMinorLocator())
    f3_ax1.xaxis.grid(linestyle='--')
    f3_ax1.yaxis.grid(linestyle='--',which='both',linewidth=0.5)

    f3_ax2 = fig3.add_subplot(gs[1, 0])
    precip.annual_mean().srex_mean().plot(ax=f3_ax2,marker='x',linestyle='',markeredgewidth=2)
    plt.title('')
    plt.xlim(0,27)
    plt.ylim(-0.015,0.025)
    plt.hlines(0,*plt.xlim(),linestyles='solid',linewidth=0.5)
    plt.xticks(np.arange(1,27))
    plt.xlabel('SREX region')
    f3_ax2.set_xticklabels(tsurf.annual_mean().srex_mean().srex_abbrev.values,
                              rotation = 90)
    f3_ax2.yaxis.set_minor_locator(AutoMinorLocator())
    f3_ax2.xaxis.grid(linestyle='--')
    f3_ax2.yaxis.grid(linestyle='--',which='both',linewidth=0.5)

# ============================================================== #
# AUXILIARY FIG) seasonal cycle and global mean anomalies

ax=plt.axes()
cloud_CO2x2.global_mean().plot()
cloud_homogeneous.global_mean().plot()
cloud_srm.global_mean().plot()
plt.ylim([0.6,0.8])


f1_ax7 = fig1.add_subplot(gs3[0, 0])
gm.tsurf.plot(ax=f1_ax7,color='k',linewidth=2)
plt.plot(1999,gm0.tsurf,marker='o',color='r',markersize=7,)
plt.ylim(14,15)
plt.xlim(1996,2053)
plt.xlabel('years')
plt.xticks(np.append(1999,np.arange(2010,2051,10)),
           np.append('0',list(map(str,np.arange(10,51,10)))))
plt.annotate('{:.2f}  '.format(gm0.tsurf.values),
            (plt.xlim()[0],gm0.tsurf.values),
            verticalalignment='center',
            horizontalalignment='right',
            fontsize=9,
            fontweight='bold')
plt.title('tsurf Global Mean')
plt.hlines(gm0.tsurf,*plt.xlim(),linestyles='dashed',linewidth=0.7)
f1_ax7.yaxis.set_minor_locator(AutoMinorLocator())
plt.grid(which='both')

f1_ax8 = fig1.add_subplot(gs3[0, 1])
gm.precip.plot(ax=f1_ax8,color='k',linewidth=2)
plt.plot(1999,gm0.precip,marker='o',color='r',markersize=7,)
plt.ylim(2.54,2.56)
plt.xlim(1996,2053)
plt.xlabel('years')
plt.xticks(np.append(1999,np.arange(2010,2051,10)),
           np.append('0',list(map(str,np.arange(10,51,10)))))
plt.annotate('{:.3f}  '.format(gm0.precip.values),
            (plt.xlim()[0],gm0.precip.values),
            verticalalignment='center',
            horizontalalignment='right',
            fontsize=9,
            fontweight='bold')
plt.title('precip Global Mean')
plt.hlines(gm0.precip,*plt.xlim(),linestyles='dashed',linewidth=0.7)
f1_ax8.yaxis.set_minor_locator(AutoMinorLocator())
f1_ax8.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

# ============================================================== #
# ============================================================== #

plot_fig1()
plt.savefig('/Users/dmar0022/Desktop/fig1.png', dpi=300, format='png',
            bbox_inches='tight')

plot_fig2()
plt.savefig('/Users/dmar0022/Desktop/fig2.png', dpi=300, format='png',
            bbox_inches='tight')

plot_fig3()
plt.savefig('/Users/dmar0022/Desktop/fig3.png', dpi=300, format='png',
            bbox_inches='tight')
