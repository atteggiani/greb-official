import warnings
warnings.simplefilter("ignore")
import myfuncs as my
from myfuncs import GREB as greb
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
srm_sw=greb.from_binary(os.path.join(greb.output_folder(),'scenario.exp-931.geoeng.2xCO2.sw.artificial.iter20_50yrs'))[['tsurf','precip']]
srm_cld=greb.from_binary(os.path.join(greb.output_folder(),'scenario.exp-930.geoeng.2xCO2.cld.artificial.iter20_50yrs'))[['tsurf','precip']]
homogeneous_sw=greb.from_binary(os.path.join(greb.output_folder(),'/Users/dmar0022/university/phd/greb-official/output/scenario.exp-931.geoeng.2xCO2.sw.artificial.frominput_x0.97953_homogeneous_50yrs.bin'))[['tsurf','precip']]
homogeneous_cld=greb.from_binary(os.path.join(greb.output_folder(),'/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.2xCO2.cld.artificial.frominput_x1.09093_homogeneous_50yrs.bin'))[['tsurf','precip']]

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
