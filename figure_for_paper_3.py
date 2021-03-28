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
sw=greb.from_binary("/Users/dmar0022/university/phd/greb-official/artificial_solar_radiation/sw.artificial.iteration/sw.artificial.iter20.bin").solar
sw_ctl = greb.from_binary(greb.solar_def_file()).solar.isel(time=slice(-30*12,None))
cld=greb.from_binary("/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.iteration/cld.artificial.iter20.bin").cloud
cld_ctl = greb.from_binary(greb.cloud_def_file()).cloud.isel(time=slice(-30*12,None))

def plot_fig3_sw(nlev=100):
    '''
    Aritificial SW matrix (best iteration)
    '''
    fig = plt.figure(figsize=(16,3),constrained_layout=False)
    heights = [10,1]
    wspace=0.15; hspace=0.15; ncols=3; nrows=2
    gs1=fig.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         bottom=0, top=1)
    # SW ANNUAL MEAN
    ax1 = fig.add_subplot(gs1[0, 0],projection=ccrs.Robinson())
    im=sw.annual_mean(30*12).anomalies().plotvar(ax=ax1,
                                add_colorbar=False,
                                levels=np.linspace(-8,-3,nlev),
                                cmap=cm.gist_rainbow,
                                title='Artificial SW Radiation')
    # SW DJF MEAN
    ax2 = fig.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    d1=sw.isel(time=slice(-30*12,None)).group_by('season').sel(time='DJF') - sw_ctl.group_by('season').sel(time='DJF')
    im2=d1.plotvar(ax=ax2,
                    add_colorbar=False,
                    levels=np.linspace(-9,0,nlev),
                    cmap=cm.gist_rainbow,
                    title='Artificial SW Radiation DJF')
    # SW JJA MEAN                                
    ax3 = fig.add_subplot(gs1[0, 2],projection=ccrs.Robinson())
    d2=sw.isel(time=slice(-30*12,None)).group_by('season').sel(time='JJA') - sw_ctl.group_by('season').sel(time='JJA')
    d2.plotvar(ax=ax3,
                add_colorbar=False,
                levels=np.linspace(-9,0,nlev),
                cmap=cm.gist_rainbow,
                title='Artificial SW Radiation JJA')
    # Colorbar 
    ax4 = fig.add_subplot(gs1[1, 0])
    plt.colorbar(im,cax=ax4, orientation='horizontal',
                 ticks=np.arange(-8,3+1,1),
                 label='$W/m^{2}$')
    ax5 = fig.add_subplot(gs1[1, 1:])
    plt.colorbar(im2,cax=ax5, orientation='horizontal',
                 ticks=np.arange(-9,0+1,+1),
                 label='$W/m^{2}$')

def plot_fig3_cld(nlev=100):
    '''
    Aritificial CLD matrix (best iteration)
    '''
    fig = plt.figure(figsize=(16,3),constrained_layout=False)
    heights = [10,1]
    wspace=0.15; hspace=0.15; ncols=3; nrows=2
    gs1=fig.add_gridspec(ncols=ncols, nrows=nrows,
                         height_ratios=heights,
                         wspace=wspace, hspace=hspace,
                         bottom=0, top=1)
    # CLD ANNUAL MEAN
    ax1 = fig.add_subplot(gs1[0, 0],projection=ccrs.Robinson())
    im=cld.annual_mean(30*12).anomalies().plotvar(ax=ax1,
                                add_colorbar=False,
                                levels=np.linspace(0,0.3,nlev),
                                norm=colors.DivergingNorm(vmin=0,vcenter=0.08,vmax=0.3),
                                cmap=cm.gist_rainbow,
                                title='Artificial Cloud Cover')
    # CLD DJF MEAN
    ax2 = fig.add_subplot(gs1[0, 1],projection=ccrs.Robinson())
    d1=cld.isel(time=slice(-30*12,None)).group_by('season').sel(time='DJF') - cld_ctl.group_by('season').sel(time='DJF')
    im2=d1.plotvar(ax=ax2,
                    add_colorbar=False,
                    levels=np.linspace(0,0.5,nlev),
                    norm=colors.DivergingNorm(vmin=0,vcenter=0.1,vmax=0.5),
                    cmap=cm.gist_rainbow,
                    title='Artificial Cloud Cover DJF')
    # CLD JJA MEAN                                
    ax3 = fig.add_subplot(gs1[0, 2],projection=ccrs.Robinson())
    d2=cld.isel(time=slice(-30*12,None)).group_by('season').sel(time='JJA') - cld_ctl.group_by('season').sel(time='JJA')
    d2.plotvar(ax=ax3,
                add_colorbar=False,
                levels=np.linspace(0,0.5,nlev),
                norm=colors.DivergingNorm(vmin=0,vcenter=0.1,vmax=0.5),
                cmap=cm.gist_rainbow,
                title='Artificial Cloud Cover JJA')
    # Colorbar 
    ax4 = fig.add_subplot(gs1[1, 0])
    plt.colorbar(im,cax=ax4, orientation='horizontal',
                 ticks=np.arange(0,0.3+0.05,0.05))
    ax5 = fig.add_subplot(gs1[1, 1:])
    plt.colorbar(im2,cax=ax5, orientation='horizontal',
                 ticks=np.arange(0,0.5+0.1,0.1))

plot_fig3_sw(nlev)
plt.savefig(os.path.join(output_folder,"fig3_sw.png"),dpi=300,bbox_inches="tight")

plot_fig3_cld(nlev)
plt.savefig(os.path.join(output_folder,"fig3_cld.png"),dpi=300,bbox_inches="tight")
