from myfuncs import *
ignore_warnings()
import matplotlib
from matplotlib.ticker import AutoMinorLocator,FormatStrFormatter

nlev=200
cmap_tsurf=constants.colormaps.Div_tsurf()
cmap_precip=constants.colormaps.Div_precip()
r_cld=from_binary('r_calibration_cloud').r
srm_filename=os.path.join(constants.output_folder(),
                 'scenario.exp-930.geoeng.cld.artificial.iter20_50yrs')
CO2x2_filename=os.path.join(constants.scenario_2xCO2())
homogeneous_filename=os.path.join(constants.output_folder(),'scenario.exp-931.geoeng.sw.artificial.frominput_x0.98007_same_gmean_50yrs')
cloud_srm_filename=constants.get_art_forcing_filename(srm_filename,
                output_path= constants.cloud_folder()+'/cld.artificial.iteration')
control=from_binary(constants.control_def_file())[['tsurf','precip','sw']]
srm=from_binary(srm_filename)[['tsurf','precip','sw']]
CO2x2=from_binary(CO2x2_filename)[['tsurf','precip','sw']]
homogeneous=from_binary(homogeneous_filename)[['tsurf','precip','sw']]
cloud_srm=from_binary(cloud_srm_filename).cloud
cloud_CO2x2=from_binary(constants.cloud_def_file()).cloud
solar_homogeneous=from_binary(constants.get_art_forcing_filename(homogeneous_filename)).solar

gm0=control.global_mean().to_celsius().mean()
gm=srm.global_mean().to_celsius().group_by('year')
matplotlib.rcParams.update({'font.size': 14})
# ============================================================== #
# FIG 1) Annual mean anomalies

def plot_fig1(nlev=100):
    fig1 = plt.figure(figsize=(16,7),constrained_layout=False)
    heights = [10,1]
    wspace=0.15; hspace=0.1; ncols=3; nrows=2
    gs1=fig1.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         top=0.95,bottom=0.55)
    gs2=fig1.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         top=0.45,bottom=0.05)

    f1_ax1 = fig1.add_subplot(gs1[0, 0],projection=ccrs.Robinson())
    im=CO2x2.anomalies().tsurf.annual_mean().plotvar(ax=f1_ax1,
                                   levels=np.linspace(1,5,nlev),
                                   cmap=cm.YlOrRd,
                                   add_colorbar=False,
                                   title='Abrupt2xCO2 tsurf')
    f1_ax2 = fig1.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    im2=homogeneous.anomalies().tsurf.annual_mean().plotvar(ax=f1_ax2,
                                   levels=np.linspace(-1,2,nlev),
                                   norm=colors.DivergingNorm(vmin=-1, vcenter=0., vmax=2),
                                   cmap=cmap_tsurf,
                                   add_colorbar=False,
                                   title='Homogeneous tsurf')
    f1_ax3 = fig1.add_subplot(gs1[0, 2],projection=ccrs.Robinson())
    im3=srm.anomalies().tsurf.annual_mean().plotvar(ax=f1_ax3,
                                   levels=np.linspace(-1,2,nlev),
                                   norm=colors.DivergingNorm(vmin=-1, vcenter=0., vmax=2),
                                   cmap=cmap_tsurf,
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
                                   levels=np.linspace(0,1.5,nlev),
                                   cmap=cm.GnBu,
                                   add_colorbar=False,
                                   title='Abrupt2xCO2 precip')
    f1_ax8 = fig1.add_subplot(gs2[0, 1],projection=ccrs.Robinson())
    min,max=-0.4,0.2
    im2=homogeneous.anomalies().precip.annual_mean().plotvar(ax=f1_ax8,
                                   levels=np.linspace(min,max,nlev),
                                   norm=colors.DivergingNorm(vmin=min, vcenter=0, vmax=max),
                                   cmap=cmap_precip,
                                   add_colorbar=False,
                                   title='Homogeneous precip')
    f1_ax9 = fig1.add_subplot(gs2[0, 2],projection=ccrs.Robinson())
    im3=srm.anomalies().precip.annual_mean().plotvar(ax=f1_ax9,
                                   levels=np.linspace(min,max,nlev),
                                   norm=colors.DivergingNorm(vmin=min, vcenter=0, vmax=max),
                                   cmap=cmap_precip,
                                   add_colorbar=False,
                                   title='SRM precip')

    f1_ax10 = fig1.add_subplot(gs2[1, 0])
    plt.colorbar(im,cax=f1_ax10, orientation='horizontal',label='mm/day',
                 ticks=np.arange(0,1.5+0.25,0.25))
    f1_ax11 = fig1.add_subplot(gs2[1, 1:])
    plt.colorbar(im2,cax=f1_ax11, orientation='horizontal',label='mm/day',
                 ticks=np.arange(min,max+0.1,0.1))

# ============================================================== #
# FIG 2) r_cld and cloud annual mean + seasonal means (JJA & DJF)
def plot_fig2(nlev=100):
    fig = plt.figure(figsize=(16,6),constrained_layout=False)
    heights = [10,1]
    wspace=0.15; hspace=0.15; ncols=3; nrows=2
    gs1=fig.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         bottom=0.56, top=1)
    gs2=fig.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         bottom=0, top=0.44)
    ax1 = fig.add_subplot(gs1[0, 0],projection=ccrs.Robinson())
    im=r_cld.annual_mean().plotvar(ax=ax1,
                                statistics=False,
                                add_colorbar=False,
                                levels=np.linspace(-9,0,nlev),
                                cmap=cm.viridis,
                                title='$S_{CLD}$ Annual Mean')
    min,max=-9,3
    ax2 = fig.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    im2=r_cld.group_by('season').sel(time='DJF').plotvar(ax=ax2,
                                statistics=False,
                                add_colorbar=False,
                                levels=np.linspace(min,max,nlev),
                                norm=colors.DivergingNorm(vmin=min, vcenter=0., vmax=max),
                                cmap=constants.colormaps.add_white(cm.viridis),
                                title='$S_{CLD}$ DJF')
    ax3 = fig.add_subplot(gs1[0, 2],projection=ccrs.Robinson())
    r_cld.group_by('season').sel(time='JJA').plotvar(ax=ax3,
                                statistics=False,
                                add_colorbar=False,
                                levels=np.linspace(min,max,nlev),
                                norm=colors.DivergingNorm(vmin=min, vcenter=0., vmax=max),
                                cmap=constants.colormaps.add_white(cm.viridis),
                                title='$S_{CLD}$ JJA')
    ax4 = fig.add_subplot(gs1[1, 0])
    plt.colorbar(im,cax=ax4, orientation='horizontal',
                 ticks=np.arange(-9,0+1,1),
                 label='K/CLD')
    ax5 = fig.add_subplot(gs1[1, 1:])
    plt.colorbar(im2,cax=ax5,
                 orientation='horizontal',
                 ticks=np.arange(min,max+1,1),
                 label='K/CLD')
    ax6 = fig.add_subplot(gs2[0, 0],projection=ccrs.Robinson())
    im=(cloud_srm.anomalies()).annual_mean().plotvar(ax=ax6,
                                    levels=np.linspace(-0.04,0.16,nlev),
                                    norm=colors.DivergingNorm(vmin=-0.04, vcenter=0, vmax=0.16),
                                    cmap=cmap_tsurf,
                                    add_colorbar=False,
                                    coast_kwargs={'edgecolor':'k'})
    ax6.set_title('<SRM> - <Abrupt2xCO2> cloud Annual Mean',fontsize=12)
    min,max=-0.25,0.25
    ax7 = fig.add_subplot(gs2[0, 1],projection=ccrs.Robinson())
    im2=(cloud_srm.anomalies()).group_by('season').sel(time='DJF').plotvar(ax=ax7,
                                    levels=np.linspace(min,max,nlev),
                                    norm=colors.DivergingNorm(vmin=min, vcenter=0, vmax=max),
                                    cmap=cmap_tsurf,
                                    add_colorbar=False,
                                    coast_kwargs={'edgecolor':'k'})
    ax7.set_title('<SRM> - <Abrupt2xCO2> cloud DJF',fontsize=12)
    ax8 = fig.add_subplot(gs2[0, 2],projection=ccrs.Robinson())
    (cloud_srm.anomalies()).group_by('season').sel(time='JJA').plotvar(ax=ax8,
                                    levels=np.linspace(min,max,nlev),
                                    norm=colors.DivergingNorm(vmin=min, vcenter=0, vmax=max),
                                    cmap=cmap_tsurf,
                                    add_colorbar=False,
                                    coast_kwargs={'edgecolor':'k'})
    ax8.set_title('<SRM> - <Abrupt2xCO2> cloud JJA',fontsize=12)
    ax9 = fig.add_subplot(gs2[1, 0])
    plt.colorbar(im,cax=ax9, orientation='horizontal',
                 ticks=np.arange(-0.04,0.16+0.04,0.04))
    ax10 = fig.add_subplot(gs2[1, 1:])
    plt.colorbar(im2,cax=ax10, orientation='horizontal',
                 ticks=np.arange(min,max+0.05,0.05))

# ============================================================== #
# FIG 3) SW Radiation (W/m^2) annual cycle
def plot_fig3():
    fig = plt.figure(figsize=(16,4),constrained_layout=False)
    gs1=fig.add_gridspec(ncols=2, nrows=1,
                         wspace=0.2,
                         left=0.1,right=0.9,
                         bottom=0.1, top=1)
    gs2=fig.add_gridspec(ncols=1, nrows=1,
                         bottom=0, top=0.05)
    ax1 = fig.add_subplot(gs1[0, 0])
    CO2x2.sw.anomalies().group_by('day').sel(lat=slice(0,90)).global_mean().plot(ax=ax1,
                        linewidth=2,
                        color='k',
                        label='Abrupt2xCO2')
    homogeneous.sw.anomalies().group_by('day').sel(lat=slice(0,90)).global_mean().plot(ax=ax1,
                        linewidth=2,
                        color='r',
                        label='Homogeneous')
    srm.sw.anomalies().group_by('day').sel(lat=slice(0,90)).global_mean().plot(ax=ax1,
                        linewidth=2,
                        color='b',
                        label='SRM')
    plt.ylabel(srm.sw.units)
    plt.ylim([-10,2])
    plt.xlabel('')
    plt.title('SW Radiation anomalies - Northern Emisphere')
    xticks=[dtime(2000,x,1).toordinal() for x in np.arange(1,13)]
    plt.gca().set_xticks(xticks)
    plt.gca().set_xticklabels([dtime.fromordinal(tick).strftime('%b') for tick in xticks])
    plt.grid()
    ax2 = fig.add_subplot(gs1[0, 1])
    CO2x2.sw.anomalies().group_by('day').sel(lat=slice(-90,0)).global_mean().plot(ax=ax2,
                        linewidth=2,
                        color='k',
                        label='Abrupt2xCO2')
    homogeneous.sw.anomalies().group_by('day').sel(lat=slice(-90,0)).global_mean().plot(ax=ax2,
                        linewidth=2,
                        color='r',
                        label='Homogeneous')
    srm.sw.anomalies().group_by('day').sel(lat=slice(-90,0)).global_mean().plot(ax=ax2,
                        linewidth=2,
                        color='b',
                        label='SRM')
    plt.ylabel(srm.sw.units)
    plt.ylim([-10,2])
    plt.xlabel('')
    plt.title('SW Radiation anomalies - Southern Emisphere')
    xticks=[dtime(2000,x,1).toordinal() for x in np.arange(1,13)]
    plt.gca().set_xticks(xticks)
    plt.gca().set_xticklabels([dtime.fromordinal(tick).strftime('%b') for tick in xticks])
    plt.grid()
    ax2.legend(ncol=3,bbox_to_anchor=[0.33,-0.12],
               frameon=False)

    ax3 = fig.add_subplot(gs2[0,0])
    plt.axes(ax3)
    ax3.set_axis_off()

# ============================================================== #
# FIG 4) anomalies averaged over SREX regions
def plot_fig4():
    fig3 = plt.figure(figsize=(16,9))
    gs1=fig3.add_gridspec(ncols=3, nrows=1,wspace=0.1,
                          bottom=0.64,top=0.98)
    gs2=fig3.add_gridspec(ncols=1, nrows=2,hspace=0.25,
                          bottom=0.05,top=0.7)

    ax=fig3.add_subplot(gs1[0,1],projection=ccrs.PlateCarree())
    constants.srex_regions().plot(ax=ax,proj=None)
    for t in ax.get_children():
        if (type(t) == matplotlib.text.Text): t.set_fontsize(7)
    ax.set_title('SREX Regions',fontsize=12)

    f3_ax1 = fig3.add_subplot(gs2[0,0])
    CO2x2.anomalies().tsurf.annual_mean().srex_mean().plot(ax=f3_ax1,
                                         marker='o',
                                         linestyle='',
                                         markeredgecolor='k',
                                         markerfacecolor='none',
                                         markeredgewidth=1.8)
    homogeneous.anomalies().tsurf.annual_mean().srex_mean().plot(ax=f3_ax1,
                                         marker='x',
                                         linestyle='',
                                         color='r',
                                         markeredgewidth=2)
    srm.anomalies().tsurf.annual_mean().srex_mean().plot(ax=f3_ax1,
                                         marker='x',
                                         linestyle='',
                                         color='b',
                                         markeredgewidth=2)
    plt.title('')
    plt.xlim(0,27)
    # plt.ylim(-0.1,0.5)
    plt.hlines(0,*plt.xlim(),linestyles='solid',linewidth=0.5)
    plt.xticks(np.arange(1,27))
    plt.xlabel('')
    f3_ax1.set_xticklabels([])
    f3_ax1.yaxis.set_minor_locator(AutoMinorLocator())
    f3_ax1.xaxis.grid(linestyle='--')
    f3_ax1.yaxis.grid(linestyle='--',which='both',linewidth=0.5)

    f3_ax2 = fig3.add_subplot(gs2[1, 0])
    CO2x2.anomalies().precip.annual_mean().srex_mean().plot(ax=f3_ax2,
                                          marker='o',
                                          linestyle='',
                                          markeredgecolor='k',
                                          markerfacecolor='none',
                                          markeredgewidth=1.8,
                                          label='Abrupt2xCO2')
    homogeneous.anomalies().precip.annual_mean().srex_mean().plot(ax=f3_ax2,
                                          marker='x',
                                          linestyle='',
                                          color='r',
                                          markeredgewidth=2,
                                          label='Homogeneous')
    srm.anomalies().precip.annual_mean().srex_mean().plot(ax=f3_ax2,
                                          marker='x',
                                          linestyle='',
                                          color='b',
                                          markeredgewidth=2,
                                          label='SRM')
    plt.title('')
    plt.xlim(0,27)
    plt.legend(ncol=3,bbox_to_anchor=(-0.005, 1.02),loc=3)
    # plt.ylim(-0.015,0.025)
    plt.hlines(0,*plt.xlim(),linestyles='solid',linewidth=0.5)
    plt.xticks(np.arange(1,27))
    plt.xlabel('SREX region')
    f3_ax2.set_xticklabels(srm.srex_mean().srex_abbrev.values,
                              rotation = 90)
    f3_ax2.yaxis.set_minor_locator(AutoMinorLocator())
    f3_ax2.xaxis.grid(linestyle='--')
    f3_ax2.yaxis.grid(linestyle='--',which='both',linewidth=0.5)

# ============================================================== #
# AUXILIARY FIGURES
# AUXILIARY FIG 1) Seasonal cycles
def plot_aux_fig1(nlev=100):
    fig1 = plt.figure(figsize=(16,7),constrained_layout=False)
    heights = [10,1]
    wspace=0.15; hspace=0.1; ncols=3; nrows=2
    gs1=fig1.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         top=0.95,bottom=0.55)
    gs2=fig1.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         top=0.45,bottom=0.05)

    min,max=-2,2
    f1_ax1 = fig1.add_subplot(gs1[0, 0],projection=ccrs.Robinson())
    im=CO2x2.anomalies().tsurf.seasonal_cycle().plotvar(ax=f1_ax1,
                                   levels=np.linspace(min,max,nlev),
                                   cmap=cmap_tsurf,
                                   add_colorbar=False,
                                   title='Abrupt2xCO2 tsurf')
    f1_ax2 = fig1.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    im2=homogeneous.anomalies().tsurf.seasonal_cycle().plotvar(ax=f1_ax2,
                                   levels=np.linspace(min,max,nlev),
                                   norm=colors.DivergingNorm(vmin=-1, vcenter=0., vmax=2),
                                   cmap=cmap_tsurf,
                                   add_colorbar=False,
                                   title='Homogeneous tsurf')
    f1_ax3 = fig1.add_subplot(gs1[0, 2],projection=ccrs.Robinson())
    im3=srm.anomalies().tsurf.seasonal_cycle().plotvar(ax=f1_ax3,
                                   levels=np.linspace(min,max,nlev),
                                   norm=colors.DivergingNorm(vmin=-1, vcenter=0., vmax=2),
                                   cmap=cmap_tsurf,
                                   add_colorbar=False,
                                   title='SRM tsurf')

    f1_ax4 = fig1.add_subplot(gs1[1, 0:])
    plt.colorbar(im,cax=f1_ax4, orientation='horizontal',label='K',
                 ticks=np.arange(min,max+0.5,0.5))

    min,max=-0.5,0.5
    f1_ax7 = fig1.add_subplot(gs2[0, 0],projection=ccrs.Robinson())
    im=CO2x2.anomalies().precip.seasonal_cycle().plotvar(ax=f1_ax7,
                                   levels=np.linspace(min,max,nlev),
                                   cmap=cmap_precip,
                                   add_colorbar=False,
                                   title='Abrupt2xCO2 precip')
    f1_ax8 = fig1.add_subplot(gs2[0, 1],projection=ccrs.Robinson())
    im2=homogeneous.anomalies().precip.seasonal_cycle().plotvar(ax=f1_ax8,
                                   levels=np.linspace(min,max,nlev),
                                   norm=colors.DivergingNorm(vmin=min, vcenter=0, vmax=max),
                                   cmap=cmap_precip,
                                   add_colorbar=False,
                                   title='Homogeneous precip')
    f1_ax9 = fig1.add_subplot(gs2[0, 2],projection=ccrs.Robinson())
    im3=srm.anomalies().precip.seasonal_cycle().plotvar(ax=f1_ax9,
                                   levels=np.linspace(min,max,nlev),
                                   norm=colors.DivergingNorm(vmin=min, vcenter=0, vmax=max),
                                   cmap=cmap_precip,
                                   add_colorbar=False,
                                   title='SRM precip')

    f1_ax10 = fig1.add_subplot(gs2[1, 0:])
    plt.colorbar(im,cax=f1_ax10, orientation='horizontal',label='mm/day',
                 ticks=np.arange(min,max+0.25,0.25))

# AUXILIARY FIG 2) seqsonal cycles averaged over SREX regions
def plot_aux_fig2():
    fig3 = plt.figure(figsize=(16,9))
    gs1=fig3.add_gridspec(ncols=3, nrows=1,wspace=0.1,
                          bottom=0.64,top=0.98)
    gs2=fig3.add_gridspec(ncols=1, nrows=2,hspace=0.25,
                          bottom=0.05,top=0.7)

    ax=fig3.add_subplot(gs1[0,1],projection=ccrs.PlateCarree())
    constants.srex_regions().plot(ax=ax,proj=None)
    for t in ax.get_children():
        if (type(t) == matplotlib.text.Text): t.set_fontsize(7)
    ax.set_title('SREX Regions',fontsize=12)

    f3_ax1 = fig3.add_subplot(gs2[0,0])
    CO2x2.anomalies().tsurf.seasonal_cycle().srex_mean().plot(ax=f3_ax1,
                                         marker='o',
                                         linestyle='',
                                         markeredgecolor='k',
                                         markerfacecolor='none',
                                         markeredgewidth=1.8)
    homogeneous.anomalies().tsurf.seasonal_cycle().srex_mean().plot(ax=f3_ax1,
                                         marker='x',
                                         linestyle='',
                                         color='r',
                                         markeredgewidth=2)
    srm.anomalies().tsurf.seasonal_cycle().srex_mean().plot(ax=f3_ax1,
                                         marker='x',
                                         linestyle='',
                                         color='b',
                                         markeredgewidth=2)
    plt.title('')
    plt.xlim(0,27)
    # plt.ylim(-0.1,0.5)
    plt.hlines(0,*plt.xlim(),linestyles='solid',linewidth=0.5)
    plt.xticks(np.arange(1,27))
    plt.xlabel('')
    f3_ax1.set_xticklabels([])
    f3_ax1.yaxis.set_minor_locator(AutoMinorLocator())
    f3_ax1.xaxis.grid(linestyle='--')
    f3_ax1.yaxis.grid(linestyle='--',which='both',linewidth=0.5)

    f3_ax2 = fig3.add_subplot(gs2[1, 0])
    CO2x2.anomalies().precip.seasonal_cycle().srex_mean().plot(ax=f3_ax2,
                                          marker='o',
                                          linestyle='',
                                          markeredgecolor='k',
                                          markerfacecolor='none',
                                          markeredgewidth=1.8,
                                          label='Abrupt2xCO2')
    homogeneous.anomalies().precip.seasonal_cycle().srex_mean().plot(ax=f3_ax2,
                                          marker='x',
                                          linestyle='',
                                          color='r',
                                          markeredgewidth=2,
                                          label='Homogeneous')
    srm.anomalies().precip.seasonal_cycle().srex_mean().plot(ax=f3_ax2,
                                          marker='x',
                                          linestyle='',
                                          color='b',
                                          markeredgewidth=2,
                                          label='SRM')
    plt.title('')
    plt.xlim(0,27)
    plt.legend(ncol=3,bbox_to_anchor=(-0.005, 1.02),loc=3)
    # plt.ylim(-0.015,0.025)
    plt.hlines(0,*plt.xlim(),linestyles='solid',linewidth=0.5)
    plt.xticks(np.arange(1,27))
    plt.xlabel('SREX region')
    f3_ax2.set_xticklabels(srm.srex_mean().srex_abbrev.values,
                              rotation = 90)
    f3_ax2.yaxis.set_minor_locator(AutoMinorLocator())
    f3_ax2.xaxis.grid(linestyle='--')
    f3_ax2.yaxis.grid(linestyle='--',which='both',linewidth=0.5)


# # AUXILIARY FIG: clouds annual cycle
# def plot_aux_fig2():
#     plt.figure(figsize=(16,9))
#     cloud_CO2x2.global_mean().plot(linewidth=2,color='k',label='Abrupt2xCO2')
#     cloud_homogeneous.global_mean().plot(linewidth=2,color='r',label='Homogeneous')
#     cloud_srm.global_mean().plot(linewidth=2,color='b',label='SRM')
#     plt.ylim([0.6,0.8])
#     plt.ylabel('')
#     plt.xlabel('')
#     plt.legend(loc=2)
#     plt.title('Cloud pattern annual cycle')
#     xticks=[dtime(2000,x,1).toordinal() for x in np.arange(1,13)]
#     plt.gca().set_xticks(xticks)
#     plt.gca().set_xticklabels([dtime.fromordinal(tick).strftime('%b') for tick in xticks])
#     plt.grid()

# # GLOBAL MEANS
# f1_ax7 = fig1.add_subplot(gs3[0, 0])
# gm.tsurf.plot(ax=f1_ax7,color='k',linewidth=2)
# plt.plot(1999,gm0.tsurf,marker='o',color='r',markersize=7,)
# plt.ylim(14,15)
# plt.xlim(1996,2053)
# plt.xlabel('years')
# plt.xticks(np.append(1999,np.arange(2010,2051,10)),
#            np.append('0',list(map(str,np.arange(10,51,10)))))
# plt.annotate('{:.2f}  '.format(gm0.tsurf.values),
#             (plt.xlim()[0],gm0.tsurf.values),
#             verticalalignment='center',
#             horizontalalignment='right',
#             fontsize=9,
#             fontweight='bold')
# plt.title('tsurf Global Mean')
# plt.hlines(gm0.tsurf,*plt.xlim(),linestyles='dashed',linewidth=0.7)
# f1_ax7.yaxis.set_minor_locator(AutoMinorLocator())
# plt.grid(which='both')
#
# f1_ax8 = fig1.add_subplot(gs3[0, 1])
# gm.precip.plot(ax=f1_ax8,color='k',linewidth=2)
# plt.plot(1999,gm0.precip,marker='o',color='r',markersize=7,)
# plt.ylim(2.54,2.56)
# plt.xlim(1996,2053)
# plt.xlabel('years')
# plt.xticks(np.append(1999,np.arange(2010,2051,10)),
#            np.append('0',list(map(str,np.arange(10,51,10)))))
# plt.annotate('{:.3f}  '.format(gm0.precip.values),
#             (plt.xlim()[0],gm0.precip.values),
#             verticalalignment='center',
#             horizontalalignment='right',
#             fontsize=9,
#             fontweight='bold')
# plt.title('precip Global Mean')
# plt.hlines(gm0.precip,*plt.xlim(),linestyles='dashed',linewidth=0.7)
# f1_ax8.yaxis.set_minor_locator(AutoMinorLocator())
# f1_ax8.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

# ============================================================== #
# ============================================================== #

plot_fig1(nlev=nlev)
plt.savefig('/Users/dmar0022/Desktop/fig1.png', dpi=300, format='png',
            bbox_inches='tight')

plot_fig2(nlev=nlev)
plt.savefig('/Users/dmar0022/Desktop/fig2.png', dpi=300, format='png',
            bbox_inches='tight')

plot_fig3()
plt.savefig('/Users/dmar0022/Desktop/fig3.png', dpi=300, format='png',
            bbox_inches='tight')

plot_fig4()
plt.savefig('/Users/dmar0022/Desktop/fig4.png', dpi=300, format='png',
            bbox_inches='tight')

plot_aux_fig1(nlev=nlev)
plt.savefig('/Users/dmar0022/Desktop/aux_fig1.png', dpi=300, format='png',
            bbox_inches='tight')

plot_aux_fig2()
plt.savefig('/Users/dmar0022/Desktop/aux_fig2.png', dpi=300, format='png',
            bbox_inches='tight')

plt.close('all')

print('Done!!')
