import warnings
warnings.simplefilter("ignore")
import myfuncs as my
from myfuncs import GREB as greb, SREX_regions as srex
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator,FormatStrFormatter
import numpy as np
import matplotlib.cm as cm
import os 
import cartopy.crs as ccrs
import matplotlib.colors as colors

output_folder = "/Users/dmar0022/university/phd/phd_project/Papers/Counteracting global warming by using a locally variable Solar Radiation Management/figs_for_paper"
matplotlib.rcParams.update({'font.size': 14})
nlev=200
# DATA
co2x2=greb.from_binary(os.path.join(greb.scenario_2xCO2()))[['tsurf','precip']]
srm_sw=greb.from_binary(os.path.join(greb.output_folder(),'scenario.exp-931.geoeng.2xCO2.sw.artificial.iter5_0.34corr_50yrs'))[['tsurf','precip']]
srm_cld=greb.from_binary(os.path.join(greb.output_folder(),'scenario.exp-930.geoeng.2xCO2.cld.artificial.iter16_0.3corr_50yrs'))[['tsurf','precip']]
homogeneous_sw=greb.from_binary("/Users/dmar0022/university/phd/greb-official/output/scenario.exp-931.geoeng.2xCO2.sw.artificial.frominput_x0.97954535_homogeneous_50yrs.bin")[['tsurf','precip']]
homogeneous_cld=greb.from_binary("/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.2xCO2.cld.artificial.frominput_x1.093056_homogeneous_50yrs.bin")[['tsurf','precip']]

def plot_fig4_sw():
    fig = plt.figure(figsize=(16,9))
    gs1=fig.add_gridspec(ncols=3, nrows=1,wspace=0.1,
                          bottom=0.64,top=0.98)
    gs2=fig.add_gridspec(ncols=1, nrows=2,hspace=0.25,
                          bottom=0.05,top=0.7)

    # SREX REGIONS PLOT
    ax=fig.add_subplot(gs1[0,1],projection=ccrs.PlateCarree())
    srex.plot(ax=ax,proj=None,fontsize=7)
    ax.set_title('SREX Regions',fontsize=12)

    # PLOT SREX MEANS
    fun=lambda x: x.annual_mean(30*12).anomalies().srex_mean()
    ax1 = fig.add_subplot(gs2[0,0])
    fun(co2x2.tsurf).plot(ax=ax1,
                        marker='o',
                        linestyle='',
                        markeredgecolor='k',
                        markerfacecolor='none',
                        markeredgewidth=1.8)
    fun(homogeneous_sw.tsurf).plot(ax=ax1,
                        marker='x',
                        linestyle='',
                        color='r',
                        markeredgewidth=2)
    fun(srm_sw.tsurf).plot(ax=ax1,
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
    plt.ylabel('')
    plt.text(-1.3,0.4,"SURFACE\nTEMPERATURE",
             horizontalalignment = "center",
             verticalalignment = "baseline",
             rotation=90,
             fontsize=16)
    ax1.set_xticklabels([])
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.grid(linestyle='--')
    ax1.yaxis.grid(linestyle='--',which='both',linewidth=0.5)

    ax2 = fig.add_subplot(gs2[1, 0])
    fun(co2x2.precip).plot(ax=ax2,
                            marker='o',
                            linestyle='',
                            markeredgecolor='k',
                            markerfacecolor='none',
                            markeredgewidth=1.8,
                            label='2xCO2')
    fun(homogeneous_sw.precip).plot(ax=ax2,
                            marker='x',
                            linestyle='',
                            color='r',
                            markeredgewidth=2,
                            label='Homogeneous $SRM_{SW}$')
    fun(srm_sw.precip).plot(ax=ax2,
                                          marker='x',
                                          linestyle='',
                                          color='b',
                                          markeredgewidth=2,
                                          label='$SRM_{SW}$')
    plt.title('')
    plt.xlim(0,27)
    plt.legend(ncol=3,bbox_to_anchor=(0.5, 1.02),loc='lower center')
    plt.hlines(0,*plt.xlim(),linestyles='solid',linewidth=0.5)
    plt.xticks(np.arange(1,27))
    plt.xlabel('SREX region')
    plt.ylabel('')
    plt.text(-1.6,0.0,"PRECIPITATION",
             horizontalalignment = "center",
             verticalalignment = "baseline",
             rotation=90,
             fontsize=16)
    ax2.set_xticklabels(srex.abbrevs,rotation = 90)
    ax2.yaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.grid(linestyle='--')
    ax2.yaxis.grid(linestyle='--',which='both',linewidth=0.5)

def plot_fig4_cld():
    fig = plt.figure(figsize=(16,9))
    gs1=fig.add_gridspec(ncols=3, nrows=1,wspace=0.1,
                          bottom=0.64,top=0.98)
    gs2=fig.add_gridspec(ncols=1, nrows=2,hspace=0.25,
                          bottom=0.05,top=0.7)

    # SREX REGIONS PLOT
    ax=fig.add_subplot(gs1[0,1],projection=ccrs.PlateCarree())
    srex.plot(ax=ax,proj=None,fontsize=7)
    ax.set_title('SREX Regions',fontsize=12)

    # PLOT SREX MEANS
    fun=lambda x: x.annual_mean(30*12).anomalies().srex_mean()
    ax1 = fig.add_subplot(gs2[0,0])
    fun(co2x2.tsurf).plot(ax=ax1,
                        marker='o',
                        linestyle='',
                        markeredgecolor='k',
                        markerfacecolor='none',
                        markeredgewidth=1.8)
    fun(homogeneous_cld.tsurf).plot(ax=ax1,
                        marker='x',
                        linestyle='',
                        color='r',
                        markeredgewidth=2)
    fun(srm_cld.tsurf).plot(ax=ax1,
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
    plt.ylabel('')
    plt.text(-1.3,0.4,"SURFACE\nTEMPERATURE",
             horizontalalignment = "center",
             verticalalignment = "baseline",
             rotation=90,
             fontsize=16)
    ax1.set_xticklabels([])
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.grid(linestyle='--')
    ax1.yaxis.grid(linestyle='--',which='both',linewidth=0.5)

    ax2 = fig.add_subplot(gs2[1, 0])
    fun(co2x2.precip).plot(ax=ax2,
                            marker='o',
                            linestyle='',
                            markeredgecolor='k',
                            markerfacecolor='none',
                            markeredgewidth=1.8,
                            label='2xCO2')
    fun(homogeneous_cld.precip).plot(ax=ax2,
                            marker='x',
                            linestyle='',
                            color='r',
                            markeredgewidth=2,
                            label='Homogeneous $SRM_{CLD}$')
    fun(srm_cld.precip).plot(ax=ax2,
                                          marker='x',
                                          linestyle='',
                                          color='b',
                                          markeredgewidth=2,
                                          label='$SRM_{CLD}$')
    plt.title('')
    plt.xlim(0,27)
    plt.legend(ncol=3,bbox_to_anchor=(0.5, 1.02),loc='lower center')
    plt.hlines(0,*plt.xlim(),linestyles='solid',linewidth=0.5)
    plt.xticks(np.arange(1,27))
    plt.xlabel('SREX region')
    plt.ylabel('')
    plt.text(-1.6,0.0,"PRECIPITATION",
             horizontalalignment = "center",
             verticalalignment = "baseline",
             rotation=90,
             fontsize=16)
    ax2.set_xticklabels(srex.abbrevs,rotation = 90)
    ax2.yaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.grid(linestyle='--')
    ax2.yaxis.grid(linestyle='--',which='both',linewidth=0.5)

def plot_fig4_sw_seascyc():
    fig = plt.figure(figsize=(16,9))
    gs1=fig.add_gridspec(ncols=3, nrows=1,wspace=0.1,
                          bottom=0.64,top=0.98)
    gs2=fig.add_gridspec(ncols=1, nrows=2,hspace=0.25,
                          bottom=0.05,top=0.7)

    # SREX REGIONS PLOT
    ax=fig.add_subplot(gs1[0,1],projection=ccrs.PlateCarree())
    srex.plot(ax=ax,proj=None,fontsize=7)
    ax.set_title('SREX Regions',fontsize=12)

    # PLOT SREX MEANS
    fun=lambda x: x.seasonal_cycle(30*12).anomalies().srex_mean()
    ax1 = fig.add_subplot(gs2[0,0])
    fun(co2x2.tsurf).plot(ax=ax1,
                        marker='o',
                        linestyle='',
                        markeredgecolor='k',
                        markerfacecolor='none',
                        markeredgewidth=1.8)
    fun(homogeneous_sw.tsurf).plot(ax=ax1,
                        marker='x',
                        linestyle='',
                        color='r',
                        markeredgewidth=2)
    fun(srm_sw.tsurf).plot(ax=ax1,
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
    plt.ylabel('')
    plt.text(-1.5,-0.1,"SURFACE\nTEMPERATURE",
             horizontalalignment = "center",
             verticalalignment = "baseline",
             rotation=90,
             fontsize=16)
    ax1.set_xticklabels([])
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.grid(linestyle='--')
    ax1.yaxis.grid(linestyle='--',which='both',linewidth=0.5)

    ax2 = fig.add_subplot(gs2[1, 0])
    fun(co2x2.precip).plot(ax=ax2,
                            marker='o',
                            linestyle='',
                            markeredgecolor='k',
                            markerfacecolor='none',
                            markeredgewidth=1.8,
                            label='2xCO2')
    fun(homogeneous_sw.precip).plot(ax=ax2,
                            marker='x',
                            linestyle='',
                            color='r',
                            markeredgewidth=2,
                            label='Homogeneous $SRM_{SW}$')
    fun(srm_sw.precip).plot(ax=ax2,
                                          marker='x',
                                          linestyle='',
                                          color='b',
                                          markeredgewidth=2,
                                          label='$SRM_{SW}$')
    plt.title('')
    plt.xlim(0,27)
    plt.legend(ncol=3,bbox_to_anchor=(0.5, 1.02),loc='lower center')
    plt.hlines(0,*plt.xlim(),linestyles='solid',linewidth=0.5)
    plt.xticks(np.arange(1,27))
    plt.xlabel('SREX region')
    plt.ylabel('')
    plt.text(-1.6,-0.25,"PRECIPITATION",
             horizontalalignment = "center",
             verticalalignment = "baseline",
             rotation=90,
             fontsize=16)
    ax2.set_xticklabels(srex.abbrevs,rotation = 90)
    ax2.yaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.grid(linestyle='--')
    ax2.yaxis.grid(linestyle='--',which='both',linewidth=0.5)

def plot_fig4_cld_seascyc():
    fig = plt.figure(figsize=(16,9))
    gs1=fig.add_gridspec(ncols=3, nrows=1,wspace=0.1,
                          bottom=0.64,top=0.98)
    gs2=fig.add_gridspec(ncols=1, nrows=2,hspace=0.25,
                          bottom=0.05,top=0.7)

    # SREX REGIONS PLOT
    ax=fig.add_subplot(gs1[0,1],projection=ccrs.PlateCarree())
    srex.plot(ax=ax,proj=None,fontsize=7)
    ax.set_title('SREX Regions',fontsize=12)

    # PLOT SREX MEANS
    fun=lambda x: x.seasonal_cycle(30*12).anomalies().srex_mean()
    ax1 = fig.add_subplot(gs2[0,0])
    fun(co2x2.tsurf).plot(ax=ax1,
                        marker='o',
                        linestyle='',
                        markeredgecolor='k',
                        markerfacecolor='none',
                        markeredgewidth=1.8)
    fun(homogeneous_cld.tsurf).plot(ax=ax1,
                        marker='x',
                        linestyle='',
                        color='r',
                        markeredgewidth=2)
    fun(srm_cld.tsurf).plot(ax=ax1,
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
    plt.ylabel('')
    plt.text(-1.5,-0.1,"SURFACE\nTEMPERATURE",
             horizontalalignment = "center",
             verticalalignment = "baseline",
             rotation=90,
             fontsize=16)
    ax1.set_xticklabels([])
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.xaxis.grid(linestyle='--')
    ax1.yaxis.grid(linestyle='--',which='both',linewidth=0.5)

    ax2 = fig.add_subplot(gs2[1, 0])
    fun(co2x2.precip).plot(ax=ax2,
                            marker='o',
                            linestyle='',
                            markeredgecolor='k',
                            markerfacecolor='none',
                            markeredgewidth=1.8,
                            label='2xCO2')
    fun(homogeneous_cld.precip).plot(ax=ax2,
                            marker='x',
                            linestyle='',
                            color='r',
                            markeredgewidth=2,
                            label='Homogeneous $SRM_{CLD}$')
    fun(srm_cld.precip).plot(ax=ax2,
                                          marker='x',
                                          linestyle='',
                                          color='b',
                                          markeredgewidth=2,
                                          label='$SRM_{CLD}$')
    plt.title('')
    plt.xlim(0,27)
    plt.legend(ncol=3,bbox_to_anchor=(0.5, 1.02),loc='lower center')
    plt.hlines(0,*plt.xlim(),linestyles='solid',linewidth=0.5)
    plt.xticks(np.arange(1,27))
    plt.xlabel('SREX region')
    plt.ylabel('')
    plt.text(-1.6,-0.25,"PRECIPITATION",
             horizontalalignment = "center",
             verticalalignment = "baseline",
             rotation=90,
             fontsize=16)
    ax2.set_xticklabels(srex.abbrevs,rotation = 90)
    ax2.yaxis.set_minor_locator(AutoMinorLocator())
    ax2.xaxis.grid(linestyle='--')
    ax2.yaxis.grid(linestyle='--',which='both',linewidth=0.5)

plot_fig4_sw()
plt.savefig(os.path.join(output_folder,"fig4_sw.png"),dpi=300,bbox_inches="tight")

plot_fig4_cld()
plt.savefig(os.path.join(output_folder,"fig4_cld.png"),dpi=300,bbox_inches="tight")

plot_fig4_sw_seascyc()
plt.savefig(os.path.join(output_folder,"fig4_sw_seascyc.png"),dpi=300,bbox_inches="tight")

plot_fig4_cld_seascyc()
plt.savefig(os.path.join(output_folder,"fig4_cld_seascyc.png"),dpi=300,bbox_inches="tight")